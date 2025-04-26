import logging
import datetime

from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def time(update, context):
    await update.message.reply_text(datetime.datetime.now().strftime("%H:%M:%S"))


async def date(update, context):
    await update.message.reply_text(datetime.datetime.now().strftime("%d.%m.%Y"))


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение {update.message.text}')


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('date', date))
    application.add_handler(CommandHandler('time', time))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


if __name__ == '__main__':
    main()
