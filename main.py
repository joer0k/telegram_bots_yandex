from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

from config import BOT_TOKEN

room_text = {
    'enter': 'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!',
    'exit': 'Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!',
    'first': 'В данном зале представлены скульптуры греческих богов\nОтсюда вы можете перейти во второй зал или отправиться к выходу',
    'second': 'В данном зале представлены скелеты динозавров\nОтсюда вы можете перейти в третий зал',
    'third': 'В данном зале представлены самые первые компьютеры\nОтсюда вы можете перейти в первый или четвертый зал',
    'fourth': 'В данном зале представлены машины военного времени\nОтсюда вы можете перейти в первый зал'
}

base_keyboard = [['/enter']]
first_keyboard = [['/room_2', '/exit']]
second_keyboard = [['/room_3']]
third_keyboard = [['/room_1', '/room_4']]
fourth_keyboard = [['/room_1']]

base_markup = ReplyKeyboardMarkup(base_keyboard, one_time_keyboard=False)
first_markup = ReplyKeyboardMarkup(first_keyboard, one_time_keyboard=False)
second_markup = ReplyKeyboardMarkup(second_keyboard, one_time_keyboard=False)
third_markup = ReplyKeyboardMarkup(third_keyboard, one_time_keyboard=False)
fourth_markup = ReplyKeyboardMarkup(fourth_keyboard, one_time_keyboard=False)


async def start(update, context):
    await update.message.reply_text(
        "Привет! Я - бот-экскурсовод. Не хочешь прогуляться по музею?", reply_markup=base_markup)


async def enter(update, context):
    await update.message.reply_text(room_text['enter'], reply_markup=fourth_markup)


async def first(update, context):
    await update.message.reply_text(room_text['first'], reply_markup=first_markup)


async def second(update, context):
    await update.message.reply_text(room_text['second'], reply_markup=second_markup)


async def third(update, context):
    await update.message.reply_text(room_text['third'], reply_markup=third_markup)


async def fourth(update, context):
    await update.message.reply_text(room_text['fourth'], reply_markup=fourth_markup)


async def exit(update, context):
    await update.message.reply_text(room_text['exit'], reply_markup=base_markup)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('enter', enter))
    application.add_handler(CommandHandler('exit', exit))

    application.add_handler(CommandHandler('room_1', first))
    application.add_handler(CommandHandler('room_2', second))
    application.add_handler(CommandHandler('room_3', third))
    application.add_handler(CommandHandler('room_4', fourth))
    application.run_polling()


if __name__ == '__main__':
    main()
