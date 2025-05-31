
import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters
from web3 import Web3

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
CHAIN_RPC = os.getenv("CHAIN_RPC")

w3 = Web3(Web3.HTTPProvider(CHAIN_RPC))
contract_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, wallet TEXT, invited_by INTEGER, rewarded INTEGER DEFAULT 0)")
conn.commit()

def send_tokens(to_address, amount):
    nonce = w3.eth.get_transaction_count(Web3.to_checksum_address(WALLET_ADDRESS))
    tx = contract.functions.transfer(Web3.to_checksum_address(to_address), amount).build_transaction({
        'chainId': 56,
        'gas': 200000,
        'gasPrice': w3.to_wei('5', 'gwei'),
        'nonce': nonce,
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    args = context.args

    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if not c.fetchone():
        invited_by = int(args[0]) if args else None
        c.execute("INSERT INTO users (user_id, invited_by) VALUES (?, ?)", (user_id, invited_by))
        conn.commit()

    c.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,))
    wallet = c.fetchone()[0]

    if not wallet:
        await update.message.reply_text("👛 لطفاً آدرس کیف پول BSC خود را وارد کنید:")
    else:
        ref_link = f"https://t.me/benjaminfranklintoken_bot?start={user_id}"
        await update.message.reply_text(f"🎉 شما قبلاً ثبت‌نام کرده‌اید.

🔗 لینک دعوت شما:
{ref_link}")

async def handle_wallet(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if not w3.is_address(text):
        await update.message.reply_text("❌ آدرس کیف پول معتبر نیست.")
        return

    c.execute("SELECT rewarded FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        await update.message.reply_text("لطفاً ابتدا /start را بزنید.")
        return

    rewarded = row[0]
    c.execute("UPDATE users SET wallet = ? WHERE user_id = ?", (text, user_id))
    conn.commit()

    if rewarded == 0:
        try:
            send_tokens(text, 500 * (10 ** 18))
            c.execute("UPDATE users SET rewarded = 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            await update.message.reply_text("✅ ۵۰۰ توکن BJF به کیف پول شما ارسال شد.")
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در ارسال توکن: {e}")
            return

        # پاداش به معرف
        c.execute("SELECT invited_by FROM users WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        if row and row[0]:
            inviter = row[0]
            c.execute("SELECT wallet FROM users WHERE user_id = ?", (inviter,))
            inviter_wallet = c.fetchone()
            if inviter_wallet and inviter_wallet[0]:
                try:
                    send_tokens(inviter_wallet[0], 100 * (10 ** 18))
                    await update.message.reply_text("🎁 معرف شما ۱۰۰ توکن BJF دریافت کرد.")
                except:
                    pass

    ref_link = f"https://t.me/benjaminfranklintoken_bot?start={user_id}"
    await update.message.reply_text(f"🔗 لینک دعوت شما:
{ref_link}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )
