from telegram import Update, ReplyKeyboardRemove, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, \
    ContextTypes, CallbackQueryHandler
from config import BOT_TOKEN
import logging
from CONSTANTS import *
from data.db_session import global_init
from funcs import get_week, commit_task, keyboard_items, available_dates, get_task_text, update_db

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    update_db()

    text = 'Привет, что ты хочешь сделать?'

    buttons = [
        [
            InlineKeyboardButton(text='Посмотреть домашку', callback_data=str(CHECK_HW))],
        [
            InlineKeyboardButton(text='Создать заметку', callback_data=str(CREATE_HW)),
            InlineKeyboardButton(text='Закрыть', callback_data=str(END))
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    if context.user_data.get("START"):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data["START"] = False
    logger.info('Старт пройден')
    return SELECTION_ACTION


async def create_homework(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = 'Выбери предмет для заметки'

    keyboard = keyboard_items()
    if context.user_data.get("START_OVER", False):
        await update.message.reply_text(text='Успешное сохранение! Продолжаем.',
                                        reply_markup=keyboard)
    else:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    logger.info('Создание домашки')
    return CREATE_HW


async def create_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["choosed_item"] = update.callback_query.data

    keyboard = get_week()

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='На какое число задали?\n\nФормат >> '
                                                       'число  месяц  год  день_недели',
                                                  reply_markup=keyboard)
    logger.info('День недели')
    return SUCCESS_DT


async def get_task_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["choosed_date"] = update.callback_query.data
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='Хорошо, напиши саму домашку')
    logger.info('Прием текста')
    return SAVE_TASK


async def save_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date = context.user_data["choosed_date"]
    item = context.user_data["choosed_item"]
    text = update.message.text

    context.user_data['choosed_item'] = None
    context.user_data["choosed_date"] = None
    context.user_data["START_OVER"] = True

    commit_task(update, item, date, text)

    logger.info('Сохранение домашки')

    await create_homework(update, context)

    return CREATE_HW


async def check_homework(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = 'Выбери предмет для просмотра'

    keyboard = keyboard_items()
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    logger.info('Выбор предмета')
    return CHOOSE_ITEM


async def check_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'Выбери дату просмотра'
    item = update.callback_query.data

    context.user_data["choosed_item"] = item

    keyboard = available_dates(update, item)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return CHECK_SPECIFIC


async def get_specific_task_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date = update.callback_query.data
    item = context.user_data["choosed_item"]
    user_id = update.effective_user.id
    text = get_task_text(date, item, user_id)
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text='Назад', callback_data=str(END))]])

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text='\n'.join([i.text for i in text]),
                                                  reply_markup=keyboard)

    return SHOWING_TEXT


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text('Пока!')
    return END


async def end_work_with_task(update, context):
    context.user_data["choosed_item"] = None
    context.user_data["START"] = True

    await start(update, context)

    return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'Хорошо, до скорой встречи!'

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)

    return END


if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()

    global_init('db/homework.db')

    end_work_with_task_handler = CallbackQueryHandler(end_work_with_task,
                                                      pattern="^" + str(END) + "$")

    check_homework_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(check_homework, pattern="^" + str(CHECK_HW) + "$")],

        states={
            CHOOSE_ITEM: [
                end_work_with_task_handler,
                CallbackQueryHandler(check_task)
            ],
            CHECK_SPECIFIC: [
                end_work_with_task_handler,
                CallbackQueryHandler(get_specific_task_desc)
            ],
            SHOWING_TEXT: [
                end_work_with_task_handler
            ]
        },
        fallbacks=[CommandHandler('stop', stop),
                   end_work_with_task_handler]
    )

    add_task_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(create_homework, pattern="^" + str(CREATE_HW) + "$")],

        states={
            CREATE_HW: [
                # CallbackQueryHandler(start, pattern="^" + str(END) + "$", ),
                end_work_with_task_handler,
                CallbackQueryHandler(create_task)
            ],
            SUCCESS_DT: [
                end_work_with_task_handler,
                CallbackQueryHandler(get_task_desc)
            ],
            SAVE_TASK: [
                end_work_with_task_handler,
                MessageHandler(filters.TEXT & ~filters.COMMAND, save_task)
            ],
        },
        fallbacks=[CommandHandler('stop', stop),
                   end_work_with_task_handler],
        map_to_parent={
            END: SELECTION_ACTION,
        }
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SELECTION_ACTION: [
                check_homework_conv,
                add_task_conv,
            ],

        },
        fallbacks=[CommandHandler('stop', stop),
                   CallbackQueryHandler(end, pattern="^" + str(END) + "$")]
    )

    app.add_handler(conv_handler)

    # app.add_handler(CommandHandler('start', start))

    app.run_polling()
