import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
text = '''Звезда полей, во мгле заледенелой
Остановившись, смотрит в полынью.
Уж на часах двенадцать прозвенело,
И сон окутал родину мою…
Звезда полей! В минуты потрясений
Я вспоминал, как тихо за холмом
Она горит над золотом осенним,
Она горит над зимним серебром…
Звезда полей горит, не угасая,
Для всех тревожных жителей земли,
Своим лучом приветливым касаясь
Всех городов, поднявшихся вдали.
Но только здесь, во мгле заледенелой,
Она восходит ярче и полней,
И счастлив я, пока на свете белом
Горит, горит звезда моих полей…'''.split('\n')

CURRENT = 10 ** 10


async def start(update, context):
    global CURRENT
    CURRENT = 1
    await update.message.reply_text(text[0])


async def stop(update, context):
    global CURRENT
    CURRENT = 10 ** 10
    await update.message.reply_text('Чтобы начать сначала введите /start')


async def suphler(update, context):
    global CURRENT
    await update.message.reply_text(text[CURRENT])


async def user_response(update, context):
    global CURRENT
    try:
        if update.message.text == text[CURRENT]:
            CURRENT += 2
            if CURRENT >= len(text):
                await update.message.reply_text("Ура, у нас получилось!\nВведи /start, чтобы начать сначала")
            if CURRENT <= len(text):
                await update.message.reply_text(text[CURRENT - 1])
        else:
            await update.message.reply_text('Нет, не так')
            await suphler(update, context)
    except IndexError:
        await update.message.reply_text('Введите /start')


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(CommandHandler('suphler', suphler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, user_response))

    application.run_polling()


if __name__ == '__main__':
    main()
