from bot import bot
from bot import ADMIN_ID
from telebot import types
from peewee import *
from dictionary import faculty_to_FACULTY
from dictionary import number_to_faculty
from keyboards import keyboard_yes_no
from keyboards import keyboard_reject_reason
from keyboards import keyboard_admin_function
import hashlib
import registration


db_admin = SqliteDatabase('admins.db')
db_banned_users = SqliteDatabase('banned.db')


class Admin(Model):
    admin_id = IntegerField(null=True, default=None)
    username = CharField(null=True, default=None)
    password = CharField(null=True, default=None)
    all_roots = BooleanField(null=True, default=False)
    reg_on = BooleanField(null=True, default=True)

    class Meta:
        database = db_admin


class BanUser(Model):
    banned_user_id = IntegerField(null=True, default=None)
    username = CharField(null=True, default=None)

    class Meta:
        database = db_banned_users


Admin.create_table()
BanUser.create_table()


def check_admin(message):
    admin1 = Admin.get_or_none(admin_id=message.chat.id)
    admin2 = Admin.get_or_none(username=message.chat.username)
    if not admin1 and not admin2:
        bot.send_message(message.chat.id, "Прости, но тебе недоступна эта функция")
        return
    elif admin1:
        sent = bot.send_message(message.chat.id, "Введи пароль")
        bot.register_next_step_handler(sent, check_passwd, admin1)
    elif admin2:
        sent = bot.send_message(message.chat.id, "Придумай пароль и напиши его сюда. Будь внимательным, "
                                                 "исправить будет нельзя")
        bot.register_next_step_handler(sent, get_new_passwd, admin2)


def get_new_passwd(message, admin):
    admin.admin_id = message.chat.id
    admin.all_roots = False
    admin.password = hashlib.sha256(message.text.encode()).hexdigest()
    admin.save()
    bot.send_message(message.chat.id, "Поздравляем, ты успешно сохранен в базе админов!")
    bot.delete_message(message.chat.id, message.message_id)


def check_passwd(message, admin):
    if message.text == 'Выход':
        return
    pass_from_user = hashlib.sha256(message.text.encode())
    if pass_from_user.hexdigest() == admin.password:
        bot.send_message(message.chat.id, "Добро пожаловать в режим админа! ",
                         reply_markup=keyboard_admin_function)
        bot.delete_message(message.chat.id, message.message_id)
    else:
        sent = bot.send_message(message.chat.id, "Неправильный пароль. Попробуй ввести еще раз. "
                                                 "Если хочешь выйти, напиши - 'Выход'")
        bot.register_next_step_handler(sent, check_passwd, admin)


@bot.callback_query_handler(func=lambda c: c.data == 'check_stud')
def first_stud(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    users = list(registration.Person.select().where((registration.Person.is_auth == 0)
                                                    & (not registration.Person.stud_photo.is_null())
                                                    & (registration.Person.stud_photo != 'REJECT')
                                                    & (registration.Person.attempts_to_auth < 3)))
    if users:
        sent = bot.send_message(call.message.chat.id, "Отправляю первый студенческий?", reply_markup=keyboard_yes_no)
        bot.register_next_step_handler(sent, go_next, users, 0)
    else:
        bot.send_message(call.message.chat.id, "Никто не отправлял студенческий",
                         reply_markup=types.ReplyKeyboardRemove())


def go_next(message, users, index):
    if message.text == 'Да':
        if index < len(users):
            sent = bot.send_photo(message.chat.id, users[index].stud_photo, '%s %s\n'
                                                                            '%s\n'
                                                                            '%s, %d лет'
                                  % (users[index].family, users[index].name,
                                     faculty_to_FACULTY[number_to_faculty[users[index].faculty]],
                                     users[index].sex, users[index].age),
                                  reply_markup=keyboard_yes_no)
            bot.register_next_step_handler(sent, confirm_auth, users, index)
        else:
            bot.send_message(message.chat.id, "На сегодня всё", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, 'Окей. Встретимся позже!', reply_markup=types.ReplyKeyboardRemove())


def confirm_auth(message, users, index):
    if message.text == 'Да':
        if index < len(users):
            users[index].stud_photo = 'OK'
            users[index].is_auth = True
            users[index].save()
            bot.send_message(users[index].chat_id, "Поздравляю! Ты прошел аутентифиакцию! "
                                                   "Теперь тебе доступны новые фукнции. "
                                                   "Вся информация о твоем студенческом была удалена, "
                                                   "ради безопасности.")
            index += 1
            sent = bot.send_message(message.chat.id, "Дальше?", reply_markup=keyboard_yes_no)
            bot.register_next_step_handler(sent, go_next, users, index)
        else:
            bot.send_message(message.chat.id, "На сегодня всё", reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Нет':
        if index < len(users):
            sent = bot.send_message(message.chat.id, "Выбери причину или напиши свою.",
                                    reply_markup=keyboard_reject_reason)
            bot.register_next_step_handler(sent, reject, users, index)


def reject(message, users, index):
    users[index].attempts_to_auth += 1
    if users[index].attempts_to_auth == 3:
        bot.send_message(users[index].chat_id, "Это была последняя попытка. Твой аккаунт заблокирован. Причина "
                                               "отказа - %s" % message.text)
        BanUser.get_or_create(banned_user_id=users[index].chat_id, username=users[index].tg)
        return
    users[index].stud_photo = 'REJECT'
    users[index].save()
    bot.send_message(users[index].chat_id, "Это была %d\\3 попыток.\nПричина - %s.\n"
                                           "После использования всех попыток, твой аккаунт "
                                           "будет забанен. Внимательно проверь совпадение "
                                           "своих анкетных данных с данными в студенческом. Если аутентификация "
                                           "пройдет успешно, ты не сможещь сменить свое имя и факультет в настройках "
                                           "анкеты." % (users[index].attempts_to_auth, message.text))
    index += 1
    sent = bot.send_message(message.chat.id, "Следующий студенческий?", reply_markup=keyboard_yes_no)
    bot.register_next_step_handler(sent, go_next, users, index)


@bot.callback_query_handler(func=lambda c: c.data == 'message_to_all')
def take_message_info(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    admin = Admin.get_or_none(Admin.admin_id == call.message.chat.id)
    if not admin:
        bot.send_message(call.message.chat.id, "Прости, но тебе недоступна эта функция")
        return
    elif not admin.all_roots:
        bot.send_message(call.message.chat.id, "Прости, но тебе недоступна эта функция")
        return
    else:
        sent = bot.send_message(call.message.chat.id, "Какое сообщение отправить?")
        bot.register_next_step_handler(sent, message_to_all)


def message_to_all(message):
    if message.text == 'Отмена':
        return
    for user in registration.Person.select():
        bot.send_message(user.chat_id, message.text)


@bot.callback_query_handler(func=lambda c: c.data == 'add_admin')
def take_admin_info_to_add(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    sent = bot.send_message(call.message.chat.id, "Отправь username")
    bot.register_next_step_handler(sent, add_admin)


def add_admin(message):
    Admin.create(username=message.text[1:])


@bot.callback_query_handler(func=lambda c: c.data == 'delete_admin')
def take_admin_info_to_delete(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    sent = bot.send_message(call.message.chat.id, "Отправь username")
    bot.register_next_step_handler(sent, delete_admin)


def delete_admin(message):
    Admin.delete().where(username=message.text[1:])


@bot.callback_query_handler(func=lambda c: c.data == 'ban_user')
def take_user_info_to_ban(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    sent = bot.send_message(call.message.chat.id, "Отправь username")
    bot.register_next_step_handler(sent, ban_user)


def ban_user(message):
    user = registration.Person.get_or_none(tg=message.text[1:])
    ban = BanUser.get_or_none(username=message.text[1:])
    if ban:
        bot.send_message(message.chat.id, 'Пользователь уже забанен')
    elif user:
        user.is_ban = True
        user.save()
        BanUser.create(username=message.text[1:], banned_user_id=user.chat_id)
    else:
        BanUser.create(username=message.text[1:])


@bot.callback_query_handler(func=lambda c: c.data == 'unban_user')
def take_user_info_to_unban(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    sent = bot.send_message(call.message.chat.id, "Отправь username")
    bot.register_next_step_handler(sent, unban_user)


def unban_user(message):
    user = registration.Person.get_or_none(tg=message.text[1:])
    ban = BanUser.get_or_none(username=message.text[1:])
    if not ban:
        bot.send_message(message.chat.id, 'Пользователь не забанен')
    elif user:
        user.is_ban = False
        user.save()
        ban.delete_instance()
    else:
        ban.delete_instance()


@bot.callback_query_handler(func=lambda c: c.data == 'set_on_reg')
def turn_on_reg(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    admin = Admin.get(admin_id=ADMIN_ID)
    admin.reg_on = True
    admin.save()


@bot.callback_query_handler(func=lambda c: c.data == 'set_off_reg')
def turn_off_reg(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    admin = Admin.get(admin_id=ADMIN_ID)
    admin.reg_on = False
    admin.save()


@bot.callback_query_handler(func=lambda c: c.data == 'delete_all_not_auth')
def delete_not_auth(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    for user in registration.Person.select().where(is_auth=0):
        user.delete_instance()


@bot.callback_query_handler(func=lambda c: c.data == 'message')
def take_message_for_one_info(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    admin = Admin.get_or_none(Admin.admin_id == call.message.chat.id)
    if not admin:
        bot.send_message(call.message.chat.id, "Прости, но тебе недоступна эта функция")
        return
    elif not admin.all_roots:
        bot.send_message(call.message.chat.id, "Прости, но тебе недоступна эта функция")
        return
    else:
        sent = bot.send_message(call.message.chat.id, "Введи id диалога с пользователем")
        bot.register_next_step_handler(sent, message_to_one_id)


def message_to_one_id(message):
    id = message.text
    sent = bot.send_message(ADMIN_ID, 'Введи текст сообщения')
    bot.register_next_step_handler(sent, message_to_one, id)


def message_to_one(message, id_user):
    bot.send_message(id_user, "Сообщение от администратора:\n%s" % message.text)
