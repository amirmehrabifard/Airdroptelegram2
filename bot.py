import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler, MessageHandler, filters
)
from db import init_db, add_user, get_user, update_referrals, get_referral_count, save_wallet, get_wallet
from web3_utils import send_tokens
from languages import get_welcome_message, get_lang_keyboard

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@benjaminfranklintoken"

logging.basicConfig(level=logging.INFO)

# استارت ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    referrer_id = args[0] if args else None

    if not get_user(user.id):
        add_user(user.id, user.username, referrer_id)

    chat_member = await context.bot.get_chat_member(CHANNEL_ID, user.id)
    if chat_member.status in ['left', 'kicked']:
        await update.message.reply_text(
            '🔐 لطفاً ابتدا در کانال عضو شوید و سپس /start را بزنید.

📢 @benjaminfranklintoken'
        )
        return

    if get_user(user.id)['rewarded'] == 0:
        await update.message.reply_text("💼 لطفاً آدرس کیف پول BSC خود را ارسال کنید تا پاداش دریافت کنید:")
        return

    keyboard = get_lang_keyboard(user.id)
    await update.message.reply_text('🌐 Choose Language:', reply_markup=keyboard)

# ذخیره آدرس والت
async def wallet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    wallet = update.message.text.strip()

    if not wallet.startswith("0x") or len(wallet) != 42:
        await update.message.reply_text("❌ آدرس معتبر BSC نیست. لطفاً دوباره ارسال کنید.")
        return

    save_wallet(user.id, wallet)

    if get_user(user.id)['rewarded'] == 0:
        tx = send_tokens(wallet, amount=500)
        if tx:
            update_referrals(user.id, rewarded=True)
            referrer = get_user(user.id)['referrer_id']
            if referrer:
                ref_wallet = get_wallet(referrer)
                if ref_wallet:
                    send_tokens(ref_wallet, amount=100)
                    update_referrals(referrer)
        await update.message.reply_text("🎉 پاداش شما ارسال شد! لطفاً چند دقیقه منتظر تایید تراکنش باشید.")
    else:
        await update.message.reply_text("✅ آدرس شما ثبت شد.")

# انتخاب زبان
async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = query.data
    user_id = query.from_user.id
    msg = get_welcome_message(lang, user_id)
    await query.answer()
    await query.edit_message_text(msg)

# لینک دعوت اختصاصی
async def myref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_username = (await context.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start={user.id}"
    count = get_referral_count(user.id)
    await update.message.reply_text(
        f"🔗 لینک دعوت شما:
{ref_link}

👥 تعداد دعوت‌های معتبر: {count}"
    )

# اجرای ربات
def main():
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myref", myref))
    app.add_handler(CallbackQueryHandler(lang_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wallet_handler))
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=os.environ.get("WEBHOOK_URL")
    )

if __name__ == "__main__":
    main()
