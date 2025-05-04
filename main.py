from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

from config import BOT_TOKEN


async def start(update, context):
    await update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?")
    return 1


async def first_response(update, context):
    locality = update.message.text
    if locality == '/skip':
        await update.message.reply_text('Какая погода у вас за окном?')
    else:
        await update.message.reply_text(
            f"Какая погода в городе {locality}?")
    return 2


async def second_response(update, context):
    await update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END  # Константа, означающая конец диалога.


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT, first_response)],
            2: [MessageHandler(filters.TEXT, second_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
