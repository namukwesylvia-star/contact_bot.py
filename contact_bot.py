# -*- coding: utf-8 -*-
"""
بوت تليجرام احترافي - استقبال طلبات التواصل
صاحب البوت: عبس

الوظيفة:
- المستخدم يرسل اسم المستخدم (يوزر) الخاص فيه + طلبه
- يتم إرسال الطلب مباشرة لصاحب البوت (عبس) عبر رسالة تيليجرام
- يظهر للمستخدم رسالة تأكيد صادقة وواضحة (بدون أي ادعاءات كاذبة)

المكتبة المستخدمة: python-telegram-bot (الإصدار 20+)
تثبيت المكتبة:
    pip install python-telegram-bot --upgrade --break-system-packages
"""

import os
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

# ============ الإعدادات ============
# يتم قراءتها من متغيرات البيئة (Environment Variables) عند النشر على سيرفر
# محلياً: تقدر تحط القيم مباشرة بدل os.environ.get(...) إذا حابب تجرب بسرعة
BOT_TOKEN = os.environ.get("BOT_TOKEN", "ضع_توكن_البوت_هنا")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", "123456789"))
OWNER_NAME = os.environ.get("OWNER_NAME", "عبس")
WELCOME_LOGO_PATH = None                   # مثال: "logo.png" إذا عندك صورة شعار محلية

# ============ إعداد اللوق ============
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ============ حالات المحادثة ============
ASK_USERNAME, ASK_MESSAGE = range(2)


# ---------- أمر البداية ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("📩 إرسال طلب تواصل", callback_data="new_request")],
        [InlineKeyboardButton("ℹ️ عن الخدمة", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = (
        f"👋 أهلاً بك في بوت التواصل الخاص بـ *{OWNER_NAME}*\n\n"
        "من هنا تقدر ترسل طلبك وبيوصلني مباشرة، وراح أتواصل معك بأقرب وقت.\n\n"
        "اضغط الزر بالأسفل للبدء 👇"
    )

    if WELCOME_LOGO_PATH:
        with open(WELCOME_LOGO_PATH, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=reply_markup,
            )
    else:
        await update.message.reply_text(
            caption, parse_mode="Markdown", reply_markup=reply_markup
        )


# ---------- زر "عن الخدمة" ----------
async def about_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_caption(
        caption=(
            f"ℹ️ هذا البوت وسيلة تواصل مباشرة مع *{OWNER_NAME}*.\n\n"
            "ترسل طلبك، وبيتم مراجعته والرد عليك خلال 24-48 ساعة تقريباً.\n\n"
            "اضغط /start للرجوع للقائمة الرئيسية."
        ),
        parse_mode="Markdown",
    ) if query.message.caption else await query.edit_message_text(
        text=(
            f"ℹ️ هذا البوت وسيلة تواصل مباشرة مع *{OWNER_NAME}*.\n\n"
            "ترسل طلبك، وبيتم مراجعته والرد عليك خلال 24-48 ساعة تقريباً.\n\n"
            "اضغط /start للرجوع للقائمة الرئيسية."
        ),
        parse_mode="Markdown",
    )


# ---------- بدء تعبئة الطلب ----------
async def new_request_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    text = "✏️ اكتب اسم المستخدم (اليوزر) الخاص فيك:"
    if query.message.caption:
        await query.message.reply_text(text)
    else:
        await query.edit_message_text(text)
    return ASK_USERNAME


async def receive_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["username"] = update.message.text.strip()
    await update.message.reply_text(
        "📝 تمام، هلا اكتب تفاصيل طلبك أو رسالتك:"
    )
    return ASK_MESSAGE


async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    username_field = context.user_data.get("username", "غير محدد")
    user_message = update.message.text.strip()

    # إرسال الطلب لصاحب البوت
    admin_text = (
        "📬 *طلب تواصل جديد*\n\n"
        f"👤 الاسم على تيليجرام: {user.full_name}\n"
        f"🔗 يوزر تيليجرام: @{user.username if user.username else 'لا يوجد'}\n"
        f"🆔 المعرف المدخل: {username_field}\n"
        f"💬 الرسالة:\n{user_message}\n\n"
        f"🕒 chat_id للرد: `{user.id}`"
    )
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID, text=admin_text, parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"فشل إرسال الطلب للأدمن: {e}")

    # رسالة تأكيد صادقة للمستخدم
    await update.message.reply_text(
        "✅ تم استلام طلبك بنجاح!\n\n"
        f"سيتم مراجعته من قبل *{OWNER_NAME}* والتواصل معك خلال مدة "
        "تقريبية من 24 إلى 48 ساعة.\n\n"
        "شكراً لصبرك 🌹",
        parse_mode="Markdown",
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ تم إلغاء الطلب. اكتب /start للبدء من جديد.")
    return ConversationHandler.END


# ---------- تشغيل البوت ----------
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(new_request_callback, pattern="^new_request$")],
        states={
            ASK_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_username)],
            ASK_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(about_callback, pattern="^about$"))

    logger.info("✅ البوت يعمل الآن...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
