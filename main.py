from telegram.ext import CommandHandler, Application

from config import BOT_TOKEN

TIMER = 5


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update, context):
    """Добавляем задачу в очередь"""
    try:
        global TIMER
        TIMER = int(context.args[0])
        chat_id = update.effective_message.chat_id
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)
        text = f'Вернусь через {TIMER} с.!'
        if job_removed:
            text += ' Старая задача удалена.'
        await update.effective_message.reply_text(text)
    except ValueError:
        await context.bot.send_message(context.job.chat_id, text=f'Переданное время некорректно')
    except IndexError:
        await context.bot.send_message(context.job.chat_id, text=f'Необходимо передать время')


async def task(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! {TIMER}c. прошли!')


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("set_timer", set_timer))
    application.add_handler(CommandHandler("unset", unset))
    application.run_polling()


if __name__ == '__main__':
    main()
