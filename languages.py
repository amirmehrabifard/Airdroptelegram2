from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_lang_keyboard(user_id):
    keyboard = [
        [
            InlineKeyboardButton("🇺🇸 English", callback_data="en"),
            InlineKeyboardButton("🇨🇳 中文", callback_data="zh"),
        ],
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="ru"),
            InlineKeyboardButton("🇫🇷 Français", callback_data="fr"),
        ],
        [
            InlineKeyboardButton("🇸🇦 العربية", callback_data="ar"),
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="fa"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_welcome_message(lang, user_id):
    ref_link = f"https://t.me/benjaminfranklintoken_bot?start={user_id}"
    messages = {
        "en": f"🎉 Welcome!
Earn 500 BJF for joining our channel.
Invite friends using your referral link to earn 100 BJF per invite!

🔗 Your link: {ref_link}",
        "zh": f"🎉 欢迎！
加入我们的频道可获得 500 BJF。
使用推荐链接邀请朋友，每邀请一人可获得 100 BJF！

🔗 你的链接: {ref_link}",
        "ru": f"🎉 Добро пожаловать!
Получите 500 BJF за вступление в канал.
Приглашайте друзей и получайте по 100 BJF за каждого!

🔗 Ваша ссылка: {ref_link}",
        "fr": f"🎉 Bienvenue !
Recevez 500 BJF en rejoignant notre chaîne.
Invitez vos amis avec votre lien de parrainage et gagnez 100 BJF par personne !

🔗 Votre lien : {ref_link}",
        "ar": f"🎉 مرحبًا!
احصل على 500 BJF عند الانضمام إلى القناة.
ادعُ أصدقاءك واربح 100 BJF عن كل شخص!

🔗 رابط الدعوة الخاص بك: {ref_link}",
        "fa": f"🎉 خوش آمدید!
با عضویت در کانال ۵۰۰ توکن BJF دریافت کنید.
با دعوت دوستانتان با لینک زیر، به ازای هر نفر ۱۰۰ توکن بگیرید!

🔗 لینک شما: {ref_link}"
    }
    return messages.get(lang, messages["en"])
