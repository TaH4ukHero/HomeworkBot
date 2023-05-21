import locale
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from datetime import datetime as dt
import datetime
from CONSTANTS import *
from data.db_session import create_session
from data.englishModel import English
from data.historyModel import History
from data.literatureModel import Literature
from data.mathModel import Math
from data.physicsModel import Physics
from data.russianModel import Russian

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)

items = ['История', 'Русский', 'Литра', 'Матан', 'Физика', 'Английский']

items_to_en = {
    "Русский": "russian",
    "История": "history",
    "Литра": "literature",
    "Матан": "math",
    "Физика": "physics",
    "Английский": "english"
}

back_button = [InlineKeyboardButton(text='Назад', callback_data=str(END))]


def get_week() -> InlineKeyboardMarkup:
    now = dt.now().date()
    buttons = []
    for i in range(1, 10):
        temp = (now + datetime.timedelta(days=i))
        if temp.weekday() not in [5, 6]:
            buttons.append([InlineKeyboardButton(text=f"{temp.strftime('%d  %b  %y  %A')}",
                                                 callback_data=temp.isoformat())])
    buttons.append(back_button)
    return InlineKeyboardMarkup(buttons)


def keyboard_items() -> InlineKeyboardMarkup:
    buttons = []

    for i, val in items_to_en.items():
        buttons.append([InlineKeyboardButton(text=i, callback_data=val)])
    buttons.append(back_button)
    keyboard = InlineKeyboardMarkup(buttons)

    return keyboard


def get_dates(update: Update, item):
    sess = create_session()
    if item == 'russian':
        hws = sess.query(Russian).filter(Russian.date >= datetime.datetime.now().date(),
                                         Russian.user_id == update.effective_user.id).all()
    elif item == 'history':
        hws = sess.query(History).filter(History.date >= datetime.datetime.now().date(),
                                         History.user_id == update.effective_user.id).all()
    elif item == 'literature':
        hws = sess.query(Literature).filter(Literature.date >= datetime.datetime.now().date(),
                                            Literature.user_id == update.effective_user.id).all()
    elif item == 'math':
        hws = sess.query(Math).filter(Math.date >= datetime.datetime.now().date(),
                                      Math.user_id == update.effective_user.id).all()
    elif item == 'physics':
        hws = sess.query(Physics).filter(Physics.date >= datetime.datetime.now().date(),
                                         Physics.user_id == update.effective_user.id).all()
    elif item == 'english':
        hws = sess.query(English).filter(English.date >= datetime.datetime.now().date(),
                                         English.user_id == update.effective_user.id).all()
    sess.close()
    return hws


def available_dates(update: Update, item) -> InlineKeyboardMarkup:
    buttons = []
    homeworks = get_dates(update, item)
    temp_list = []
    for i in homeworks:
        temp = i.date.strftime('%d  %b  %y  %A')
        if temp not in temp_list:
            buttons.append([InlineKeyboardButton(text=f"{temp}",
                                                 callback_data=i.date.isoformat())])
            temp_list.append(temp)
    buttons.append(back_button)
    temp_list.clear()
    return InlineKeyboardMarkup(buttons)


def get_task_text(date, item, user_id):
    sess = create_session()
    task_date = datetime.datetime.fromisoformat(date).date()
    if item == 'russian':
        text = sess.query(Russian).filter(Russian.date == task_date,
                                          Russian.user_id == user_id).all()
    elif item == 'history':
        text = sess.query(History).filter(History.date == task_date,
                                          History.user_id == user_id).all()
    elif item == 'literature':
        text = sess.query(Literature).filter(Literature.date == task_date,
                                             Literature.user_id == user_id).all()
    elif item == 'math':
        text = sess.query(Math).filter(Math.date == task_date,
                                       Math.user_id == user_id).all()
    elif item == 'physics':
        text = sess.query(Physics).filter(Physics.date == task_date,
                                          Physics.user_id == user_id).all()
    elif item == 'english':
        text = sess.query(English).filter(English.date == task_date,
                                          English.user_id == user_id).all()
    return text


def commit_task(update: Update, item, date, text):
    sess = create_session()
    task_date = datetime.datetime.fromisoformat(date).date()
    if item == 'russian':
        user = Russian()
        user.user_id = update.effective_user.id
        user.date = task_date
        user.text = text
    elif item == 'history':
        user = History()
        user.user_id = update.effective_user.id
        user.date = task_date
        user.text = text
    elif item == 'literature':
        user = Literature()
        user.user_id = update.effective_user.id
        user.date = task_date
        user.text = text
    elif item == 'math':
        user = Math()
        user.user_id = update.effective_user.id
        user.date = task_date
        user.text = text
    elif item == 'physics':
        user = Physics()
        user.user_id = update.effective_user.id
        user.date = task_date
        user.text = text
    elif item == 'english':
        user = English()
        user.user_id = update.effective_user.id
        user.date = task_date
        user.text = text
    sess.add(user)
    sess.commit()


def update_db():
    sess = create_session()
    hws = sess.query(Russian).filter(Russian.date < datetime.datetime.now().date()).all()
    sess.delete(hws)
    hws = sess.query(History).filter(History.date < datetime.datetime.now().date()).all()
    sess.delete(hws)
    hws = sess.query(English).filter(English.date < datetime.datetime.now().date()).all()
    sess.delete(hws)
    hws = sess.query(Physics).filter(Physics.date < datetime.datetime.now().date()).all()
    sess.delete(hws)
    hws = sess.query(Math).filter(Math.date < datetime.datetime.now().date()).all()
    sess.delete(hws)
    hws = sess.query(Literature).filter(Literature.date < datetime.datetime.now().date()).all()
    sess.delete(hws)
    sess.commit()

# def search_user(update: Update, item):
#     sess = create_session()
#     if item == 'russian':
#         user = sess.query(Russian).filter(Russian.user_id == update.effective_user.id).first()
#         if user is None:
#
#             user = sess.query(Russian).filter(Russian.user_id == update.effective_user.id).first()
#     elif item == 'history':
#         user = sess.query(History).filter(History.user_id == update.effective_user.id).first()
#         if user is None:
#             user = History()
#             user.user_id = update.effective_user.id
#             sess.add(user)
#             sess.commit()
#             user = sess.query(History).filter(History.user_id == update.effective_user.id).first()
#     elif item == 'literature':
#         user = sess.query(Literature).filter(Literature.user_id == update.effective_user.id).first()
#         if user is None:
#             user = Literature()
#             user.user_id = update.effective_user.id
#             sess.add(user)
#             sess.commit()
#             user = sess.query(Literature).filter(
#                 Literature.user_id == update.effective_user.id).first()
#     elif item == 'math':
#         user = sess.query(Math).filter(Math.user_id == update.effective_user.id).first()
#         if user is None:
#             user = Math()
#             user.user_id = update.effective_user.id
#             sess.add(user)
#             sess.commit()
#             user = sess.query(Math).filter(Math.user_id == update.effective_user.id).first()
#     elif item == 'physics':
#         user = sess.query(Physics).filter(Physics.user_id == update.effective_user.id).first()
#         if user is None:
#             user = Physics()
#             user.user_id = update.effective_user.id
#             sess.add(user)
#             sess.commit()
#             user = sess.query(Physics).filter(Physics.user_id == update.effective_user.id).first()
#     elif item == 'english':
#         user = sess.query(English).filter(English.user_id == update.effective_user.id).first()
#         if user is None:
#             user = English()
#             user.user_id = update.effective_user.id
#             sess.add(user)
#             sess.commit()
#             user = sess.query(English).filter(English.user_id == update.effective_user.id).first()
#     return user, sess
