from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler
)

from config import TOKEN
from downloader import download_video
from telegram.error import BadRequest

CHANNEL_USERNAME = "@kabirov_dev"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        print("STATUS:", member.status)

        if member.status not in ["member", "administrator", "creator"]:

            keyboard = [
                [
                    InlineKeyboardButton(
                        "📢 Подписаться на канал",
                        url="https://t.me/kabirov_dev"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "✅ Проверить подписку",
                        callback_data="check_sub"
                    )
                ]
            ]

            await update.message.reply_text(
                "🔒 Для использования AllVideoSaveBot\n"
                "сначала подпишитесь на наш канал.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            return

    except BadRequest as e:
        print("CHECK SUB ERROR:", e)
        await update.message.reply_text(
            "❌ Не удалось проверить подписку."
        )
        return


    keyboard = [
        [
            InlineKeyboardButton("🎬 Скачать видео", callback_data="download"),
            InlineKeyboardButton("📖 Инструкция", callback_data="help")
        ],
        [
            InlineKeyboardButton("🌐 Поддерживаемые сайты", callback_data="sites")
        ],
        [
            InlineKeyboardButton("ℹ️ О боте", callback_data="about"),
            InlineKeyboardButton("⚙️ Настройки", callback_data="settings")
        ]
    ]

    await update.message.reply_text(
        "👋 Добро пожаловать в AllVideoSaveBot!\n\n"
        "🎬 Отправьте ссылку на видео.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "check_sub":

        await query.edit_message_text(
            "✅ Подписка проверена!"
        )

    elif query.data == "download":

        await query.edit_message_text(
            "🔗 Отправьте ссылку на видео."
        )

    elif query.data == "help":

        await query.edit_message_text(
            "📖 Инструкция:\n\n"
            "1. Нажмите Скачать видео\n"
            "2. Отправьте ссылку\n"
            "3. Получите видео ✅"
        )

    elif query.data == "sites":

        await query.edit_message_text(
            "🌐 Поддерживаемые сайты:\n\n"
            "✅ YouTube\n"
            "✅ TikTok\n"
            "✅ Instagram\n"
            "✅ Pinterest"
        )

    elif query.data == "about":

        await query.edit_message_text(
            "ℹ️ AllVideoSaveBot\n\n"
            "Бот для скачивания видео."
        )

    elif query.data == "settings":

        await query.edit_message_text(
            "⚙️ Настройки скоро будут доступны."
        )


async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    print("LINK:", url)

    status_message = await update.message.reply_text(
        "⏳ Скачивание видео началось..."
    )

    try:

        file_path = download_video(url)

        with open(file_path, "rb") as video:

            await update.message.reply_video(
                video=video,
                caption="✅ AllVideoSaveBot"
            )

        try:
            await status_message.delete()

        except Exception as e:
            print("DELETE ERROR:", e)


    except Exception as e:

        print("ОШИБКА:", repr(e))

        await update.message.reply_text(
            f"❌ Ошибка:\n{repr(e)}"
        )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            video_handler
        )
    )

    print("AllVideoSaveBot запущен!")

    app.run_polling()


if __name__ == "__main__":
   main()