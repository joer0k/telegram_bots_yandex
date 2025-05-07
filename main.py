import logging
import random
from json import loads

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

QUESTIONS = {}
IS_GAME = False
user_answered = {}
last = ''


async def start(update, context):
    await update.message.reply_text('Не хотите ли вы пройти опрос?\n/yes - да\n/no - нет')


async def stop(update, context):
    global IS_GAME
    IS_GAME = False
    await update.message.reply_text('Приходите, когда будете готовы')


async def yes(update, context):
    if QUESTIONS:
        global IS_GAME, user_answered, last
        IS_GAME = True
        question = random.choice(list(QUESTIONS.keys()))
        user_answered = {question: ''}
        last = question
        await update.message.reply_text(question)
    else:
        await update.message.reply_text('Сначала введите вопросы в формате json')


async def get_questions(update, context):
    global IS_GAME, QUESTIONS, user_answered, last
    if not IS_GAME:
        try:
            for res in loads(update.message.text)['test']:
                QUESTIONS[res['question']] = res['response']
            await update.message.reply_text('Вопросы успешно записаны\nНачать тест - /yes')
        except Exception as e:
            await update.message.reply_text(f'Ошибка: {e}')
    else:
        user_answered[last] = update.message.text.strip()
        if len(user_answered.keys()) == len(QUESTIONS.keys()) or len(user_answered.keys()) == 10:
            IS_GAME = False
            await update.message.reply_text(
                f'Тест окончен. Правильных ответов - {len([value for key, value in user_answered.items() if value == QUESTIONS[key]])}')
        else:
            question = random.choice(list(QUESTIONS.keys()))
            while question in user_answered.keys():
                question = random.choice(list(QUESTIONS.keys()))
            user_answered[question] = ''
            last = question
            await update.message.reply_text(question)


async def no(update, context):
    await update.message.reply_text('Ничего страшного, жду вас снова')


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(CommandHandler('yes', yes))
    application.add_handler(CommandHandler('no', no))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_questions))
    application.run_polling()


if __name__ == '__main__':
    main()
