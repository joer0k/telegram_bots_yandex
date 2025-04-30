from random import randint

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Application

from config import BOT_TOKEN

TIMER = 5

start_keyboard = [['/dice', '/timer']]
dice_keyboard = [['/6', '/2x6', '/20'], ['/back']]
timer_keyboard = [['/30s', '/1m', '/5m'], ['/back']]
close_keyboard = [['close']]

start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=False)
dice_markup = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)
timer_markup = ReplyKeyboardMarkup(timer_keyboard, one_time_keyboard=False)
close_markup = ReplyKeyboardMarkup(close_keyboard, one_time_keyboard=False)


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def start(update, context):
    await update.message.reply_text('Привет! Я - бот-помощник для игр')
    await update.message.reply_text('/dice - кинуть кубик\n/timer - засечь время', reply_markup=start_markup)


async def dice(update, context):
    await update.message.reply_text('Выберите какой кубик кинуть: 6-игранный, 2 6-и гранных, 20-и гранный',
                                    reply_markup=dice_markup)


async def dice_6(update, context):
    await update.message.reply_text(f'{randint(1, 6)}')


async def dice_2x6(update, context):
    await update.message.reply_text(f'{randint(1, 6)} {randint(1, 6)}')


async def dice_20(update, context):
    await update.message.reply_text(f'{randint(1, 20)}')


async def timers(update, context):
    await update.message.reply_text('Засечь время: 30s, 1m, 5m', reply_markup=timer_markup)


async def set_timer(update, context, time):
    job = context.job_queue.run_once(time, chat_id=update.message.chat_id, data=time)

    context.chat_data['job'] = job
    await update.message.reply_text(f'Засек {time} секунд', reply_markup=close_markup)


async def timer_ran_out(update, context):
    await context.bot.send_message(chat_id=update.message.chat_id, text='Время вышло', reply_markup=timer_markup)


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


async def timer_30s(update, context):
    await set_timer(update, context, 30)


async def timer_1m(update, context):
    await set_timer(update, context, 60)


async def timer_5m(update, context):
    await set_timer(update, context, 300)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    application.add_handler(CommandHandler('dice', dice))

    application.add_handler(CommandHandler('back', start))

    application.add_handler(CommandHandler('timer', timers))

    application.add_handler(CommandHandler('6', dice_6))
    application.add_handler(CommandHandler('2x6', dice_2x6))
    application.add_handler(CommandHandler('20', dice_20))

    application.add_handler(CommandHandler('30s', timer_30s))
    application.add_handler(CommandHandler('1m', timer_1m))
    application.add_handler(CommandHandler('5m', timer_5m))

    application.run_polling()


if __name__ == '__main__':
    main()
