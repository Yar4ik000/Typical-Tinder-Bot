from bot import bot
from keyboards import keyboard_search_filter
from keyboards import keyboard_yes_no_search
from keyboards import keyboard_tech_faculty_search
from keyboards import keyboard_faculty_question
from keyboards import keyboard_types_faculty_search
from keyboards import keyboard_human_faculty_search
from keyboards import keyboard_sex_search
from keyboards import keyboard_course_wtht_back
from dictionary import faculty_to_number
from dictionary import number_to_faculty
import emoji
from telebot import types


def first_change_message(user):
    sent = bot.send_message(user.chat_id, "Выбери, что хочешь поменять.",
                            reply_markup=keyboard_search_filter)
    bot.register_next_step_handler(sent, choose_filter_field, user)


def choose_filter_field(message, user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Выбери что хочешь поменять',
                                reply_markup=keyboard_search_filter)
        bot.register_next_step_handler(sent, choose_filter_field, user)
        return
    if message.text == 'Минимальный возраст':
        user.srh_all = False
        user.save()
        sent = bot.send_message(message.chat.id, "Напиши минимальный возраст для поиска",
                                reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(sent, min_age, user)
        return
    elif message.text == 'Максимальный возраст':
        user.srh_all = False
        user.save()
        sent = bot.send_message(message.chat.id, "Напиши максимальный возраст для поиска",
                                reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(sent, max_age, user)
        return
    elif message.text == 'Минимальный курс':
        user.srh_all = False
        user.save()
        sent = bot.send_message(message.chat.id, "Выбери минимальный курс для поиска",
                                reply_markup=keyboard_course_wtht_back)
        bot.register_next_step_handler(sent, min_course, user)
        return
    elif message.text == 'Максимальный курс':
        user.srh_all = False
        user.save()
        sent = bot.send_message(message.chat.id, "Выбери максимальный курс для поиска",
                                reply_markup=keyboard_course_wtht_back)
        bot.register_next_step_handler(sent, max_course, user)
        return
    elif message.text == 'Факультеты':
        sent = bot.send_message(message.chat.id, "Что ты хочешь сделать?",
                                reply_markup=keyboard_faculty_question)
        bot.register_next_step_handler(sent, faculty_question, user)
        return
    elif message.text == 'Авторизованность':
        if not user.is_auth:
            sent = bot.send_message(message.chat.id, "Прости, но эта функция доступна только авторизованным "
                                                     "пользователям\n "
                                                     "Хочешь еще что-то поменять?",
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
        user.srh_all = False
        user.save()
        sent = bot.send_message(message.chat.id, "Искать только авторизованных пользователей?",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, auth, user)
        return
    elif message.text == 'Пол':
        user.srh_all = False
        user.save()
        sent = bot.send_message(message.chat.id, "Чьи анкеты показывать?", reply_markup=keyboard_sex_search)
        bot.register_next_step_handler(sent, sex, user)
        return
    elif message.text == 'Ничего':
        bot.send_message(message.chat.id, 'Окей ' + emoji.emojize(':call_me_hand:'),
                         reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Искать всех':
        user.srh_all = True
        user.save()
        sent = bot.send_message(message.chat.id, "Теперь ты ищешь анкеты всех пользователей. Хочешь что-то поменять?",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return


def min_age(message, user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, отправь только цифры.')
        bot.register_next_step_handler(sent, min_age, user)
        return
    elif not message.text.isdigit():
        sent = bot.send_message(message.chat.id, "Введи корректный возраст")
        bot.register_next_step_handler(sent, min_age, user)
        return
    if int(message.text) > 30 or int(message.text) < 16:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, введи корректный возраст.')
        bot.register_next_step_handler(sent, min_age, user)
        return
    user.srh_min_age = int(message.text)
    user.save()
    if user.srh_max_age:
        if int(message.text) > user.srh_max_age:
            sent = bot.send_message(message.chat.id, "Минимальный возраст - %d.\nКажется, твой минимальный возраст "
                                                     "больше максимального. Ты не сможешь найти ни одну анкету. "
                                                     "Поменяй максимальный возраст, чтобы исправить это."
                                                     "Хочешь еще что-то изменить?" % int(message.text),
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
        else:
            sent = bot.send_message(message.chat.id, 'Минимальный возраст для поиска - %d.\n'
                                                     'Хочешь еще что то поменять?' % int(message.text),
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
    else:
        sent = bot.send_message(message.chat.id, 'Минимальный возраст для поиска - %d.\n'
                                                 'Хочешь еще что то поменять?' % int(message.text),
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return


def max_age(message, user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, отправь только цифры.')
        bot.register_next_step_handler(sent, max_age, user)
        return
    elif not message.text.isdigit():
        sent = bot.send_message(message.chat.id, "Введи корректный возраст")
        bot.register_next_step_handler(sent, max_age, user)
        return
    if int(message.text) > 30 or int(message.text) < 16:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, введи корректный возраст.')
        bot.register_next_step_handler(sent, max_age, user)
        return
    user.srh_max_age = int(message.text)
    user.save()
    if user.srh_min_age:
        if int(message.text) < user.srh_min_age:
            sent = bot.send_message(message.chat.id, "Максимальный возраст - %d.\nКажется, твой минимальный возраст "
                                                     "больше максимального. Ты не сможешь найти ни одну анкету. "
                                                     "Поменяй максимальный возраст, чтобы исправить это."
                                                     "Хочешь еще что-то изменить?" % int(message.text),
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
        else:
            sent = bot.send_message(message.chat.id, 'Максимальный возраст для поиска - %d.\n'
                                                     'Хочешь еще что то поменять?' % int(message.text),
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
    else:
        sent = bot.send_message(message.chat.id, 'Максимальный возраст для поиска - %d.\n'
                                                 'Хочешь еще что то поменять?' % int(message.text),
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return


def min_course(message, user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Выбери минимальный курс',
                                reply_markup=keyboard_course_wtht_back)
        bot.register_next_step_handler(sent, min_course, user)
        return
    elif not message.text.isdigit():
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Выбери минимальный курс',
                                reply_markup=keyboard_course_wtht_back)
        bot.register_next_step_handler(sent, min_course, user)
        return
    if int(message.text) > 6 or int(message.text) < 1:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Выбери минимальный курс',
                                reply_markup=keyboard_course_wtht_back)
        bot.register_next_step_handler(sent, min_course, user)
        return
    user.srh_min_course = int(message.text)
    user.save()
    if user.srh_max_course:
        if int(message.text) > user.srh_max_course:
            sent = bot.send_message(message.chat.id, "Минимальный курс - %d.\nКажется, твой минимальный курс "
                                                     "больше максимального. Ты не сможешь найти ни одну анкету. "
                                                     "Поменяй максимальный курс, чтобы исправить это."
                                                     "Хочешь еще что-то изменить?" % int(message.text),
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
        else:
            sent = bot.send_message(message.chat.id, 'Минимальный курс для поиска - %d.\n'
                                                     'Хочешь еще что то поменять?' % int(message.text),
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
    else:
        sent = bot.send_message(message.chat.id, 'Минимальный курс для поиска - %d.\n'
                                                 'Хочешь еще что то поменять?' % int(message.text),
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return


def max_course(message, user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Выбери максимальный курс',
                                reply_markup=keyboard_course_wtht_back)
        bot.register_next_step_handler(sent, max_course, user)
        return
    elif not message.text.isdigit():
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Выбери максимальный курс',
                                reply_markup=keyboard_course_wtht_back)
        bot.register_next_step_handler(sent, max_course, user)
        return
    if int(message.text) > 6 or int(message.text) < 1:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Выбери максимальный курс',
                                reply_markup=keyboard_course_wtht_back)
        bot.register_next_step_handler(sent, max_course, user)
        return
    user.srh_max_course = int(message.text)
    user.save()
    if user.srh_min_course:
        if int(message.text) < user.srh_min_course:
            sent = bot.send_message(message.chat.id, "Максимальный курс - %d.\nКажется, твой минимальный курс "
                                                     "больше максимального. Ты не сможешь найти ни одну анкету. "
                                                     "Поменяй максимальный курс, чтобы исправить это."
                                                     "Хочешь еще что-то изменить?" % int(message.text),
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
        else:
            sent = bot.send_message(message.chat.id, 'Максимальный курс для поиска - %d.\n'
                                                     'Хочешь еще что то поменять?' % int(message.text),
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
    else:
        sent = bot.send_message(message.chat.id, 'Максимальный курс для поиска - %d.\n'
                                                 'Хочешь еще что то поменять?' % int(message.text),
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return


def faculty_question(message, user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Что ты хочешь сделать?',
                                reply_markup=keyboard_faculty_question)
        bot.register_next_step_handler(sent, faculty_question, user)
        return
    elif message.text == 'Ничего':
        sent = bot.send_message(message.chat.id, 'Хочешь поменять еще что-либо?', reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return
    elif message.text != 'Добавить факультеты к поиску' and message.text != 'Убрать факультеты из поиска' and \
            message.text != 'Добавить все факультеты' and message.text != 'Убрать все факультеты':
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Что ты хочешь сделать?',
                                reply_markup=keyboard_faculty_question)
        bot.register_next_step_handler(sent, faculty_question, user)
        return
    faculty_choose_str = ''
    for i in range(36):
        if user.srh_faculty & (2 ** i) != 0:
            faculty_choose_str += number_to_faculty[2 ** i] + '\n'
    if faculty_choose_str == '':
        bot.send_message(message.chat.id, "У тебя не выбрано ни одного факультета для поиска")
    else:
        bot.send_message(message.chat.id, 'Твои уже выбранные для поиска факультеты: '
                                          '\n%s' % faculty_choose_str)
    if message.text == 'Добавить факультеты к поиску':
        if user.srh_faculty == 2 ** 37 - 1:
            sent = bot.send_message(message.chat.id, 'Ты уже ищешь все факультеты. '
                                                     'Хочешь еще что-то поменять?', reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
        else:
            user.srh_all = False
            user.save()
            sent = bot.send_message(message.chat.id, 'Выбери тип добавляемого факультета',
                                    reply_markup=keyboard_types_faculty_search)
            bot.register_next_step_handler(sent, faculty_type, user, 'add')
            return
    elif message.text == 'Убрать факультеты из поиска':
        if user.srh_faculty == 0:
            sent = bot.send_message(message.chat.id, 'Ты уже не ищешь все факультеты. '
                                                     'Хочешь еще что-то поменять?', reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
        else:
            user.srh_all = False
            user.save()
            sent = bot.send_message(message.chat.id, 'Выбери тип убираемого факультета',
                                    reply_markup=keyboard_types_faculty_search)
            bot.register_next_step_handler(sent, faculty_type, user, 'sub')
            return
    elif message.text == 'Добавить все факультеты':
        user.srh_all = False
        user.save()
        user.srh_faculty = 2 ** 37 - 1
        user.save()
        sent = bot.send_message(message.chat.id, "Теперь ты ищешь все факультеты. Хочешь еще что-то поменять?",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return
    elif message.text == 'Убрать все факультеты':
        user.srh_all = False
        user.save()
        user.srh_faculty = 0
        user.save()
        sent = bot.send_message(message.chat.id, "Теперь ты не ищешь ни один факультет. Хочешь еще что-то поменять?",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры. Выбери что ты хочешь "
                                                 "сделать с настройками поиска факультетов",
                                reply_markup=keyboard_faculty_question)
        bot.register_next_step_handler(sent, faculty_question, user)
        return


def faculty_type(message, user, add_sub):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Выбери тип факультета',
                                reply_markup=keyboard_types_faculty_search)
        bot.register_next_step_handler(sent, faculty_type, user, add_sub)
        return
    elif message.text == 'Технический/Естественнонаучный':
        sent = bot.send_message(message.chat.id, "Выбери факультет", reply_markup=keyboard_tech_faculty_search)
        bot.register_next_step_handler(sent, faculty, user, add_sub)
        return
    elif message.text == 'Социальный/Гуманитарный':
        sent = bot.send_message(message.chat.id, "Выбери факультет", reply_markup=keyboard_human_faculty_search)
        bot.register_next_step_handler(sent, faculty, user, add_sub)
        return
    else:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры. Выбери тип факультета',
                                reply_markup=keyboard_types_faculty_search)
        bot.register_next_step_handler(sent, faculty_type, user, add_sub)
        return


def faculty(message, user, add_sub):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Выбери факультет')
        bot.register_next_step_handler(sent, faculty, user, add_sub)
        return
    elif message.text not in faculty_to_number:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Выбери факультет')
        bot.register_next_step_handler(sent, faculty, user, add_sub)
        return
    elif add_sub == 'add':
        if user.srh_faculty == 2 ** 37 - 1:
            sent = bot.send_message(message.chat.id, 'Ты уже ищешь все факультеты. Хочешь поменять еще что-то?',
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
        elif faculty_to_number[message.text] & user.srh_faculty != 0:
            sent = bot.send_message(message.chat.id, "Этот факультет ты уже ищешь. Хочешь добавить еще какие-то?",
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, next_faculty, user, add_sub)
            return
        else:
            user.srh_faculty += faculty_to_number[message.text]
            user.save()
            sent = bot.send_message(message.chat.id, "Добавить еще какие-то факультеты?",
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, next_faculty, user, add_sub)
            return
    elif add_sub == 'sub':
        if user.srh_faculty == 0:
            sent = bot.send_message(message.chat.id, 'Ты уже не ищешь все факультеты. Хочешь поменять еще что-то?',
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user)
            return
        elif faculty_to_number[message.text] & user.srh_faculty == 0:
            sent = bot.send_message(message.chat.id, "Этот факультет ты уже не ищешь. Хочешь убрать "
                                                     "из поиска еще какие-то?",
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, next_faculty, user, add_sub)
            return
        else:
            user.srh_faculty -= faculty_to_number[message.text]
            user.save()
            sent = bot.send_message(message.chat.id, "Убрать еще какие-то факультеты?",
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, next_faculty, user, add_sub)
            return


def next_faculty(message, user, add_sub):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Убрать' if add_sub == 'sub' else 'Добавить' + 'еще какие-то '
                                                                                                'факультеты?',
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, next_faculty, user, add_sub)
        return
    elif message.text == 'Да':
        sent = bot.send_message(message.chat.id, "Выбери тип факультета",
                                reply_markup=keyboard_types_faculty_search)
        bot.register_next_step_handler(sent, faculty_type, user, add_sub)
        return
    elif message.text == 'Нет':
        sent = bot.send_message(message.chat.id, 'Хочешь еще что-то поменять?',
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, пользуйся кнопками с клавиатуры. "
                                                 "Хочешь %s еще факультеты для поиска?"
                                % ('добавить' if add_sub == 'add' else 'удалить'),
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, next_faculty, user)
        return


def auth(message, user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Искать только авторизованных пользователей?',
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, auth, user)
        return
    elif message.text == 'Да':
        user.srh_only_auth = True
        user.save()
        sent = bot.send_message(message.chat.id, "Теперь тебе будут показываться анкеты только "
                                                 "авторизованных пользователей. Хочешь еще что-то поменять?",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return
    elif message.text == 'Нет':
        user.srh_only_auth = False
        user.save()
        sent = bot.send_message(message.chat.id, 'Теперь тебе будут показываться анкеты все пользователей. '
                                                 'Хочешь еще что-то поменять?',
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, пользуйся кнопками с клавиатуры. "
                                                 "Искать только авторизованных пользователей?",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, auth, user)
        return


def sex(message, user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Кого хочешь искать?',
                                reply_markup=keyboard_sex_search)
        bot.register_next_step_handler(sent, sex, user)
        return
    elif message.text == 'Парней':
        user.srh_sex = 'Парень'
        user.save()
        sent = bot.send_message(message.chat.id, 'Теперь тебе будут показывать только анкеты парней. '
                                                 'Хочешь еще что-то поменять?',
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return
    elif message.text == 'Девушек':
        user.srh_sex = 'Девушка'
        user.save()
        sent = bot.send_message(message.chat.id, 'Теперь тебе будут показывать только анкеты девушек. '
                                                 'Хочешь еще что-то поменять?',
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return
    elif message.text == 'Всех':
        user.srh_sex = 'Любой'
        user.save()
        sent = bot.send_message(message.chat.id, 'Теперь тебе будут показывать анкеты и парней, и девушек. '
                                                 'Хочешь еще что-то поменять?',
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
    else:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Кого хочешь искать?',
                                reply_markup=keyboard_sex_search)
        bot.register_next_step_handler(sent, sex, user)
        return


def change_more(message, user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Хочешь еще что-то поменять?',
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return
    elif message.text == 'Да':
        sent = bot.send_message(user.chat_id, "Выбери, что хочешь поменять", reply_markup=keyboard_search_filter)
        bot.register_next_step_handler(sent, choose_filter_field, user)
        return
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, "Все изменения сохранены.", reply_markup=types.ReplyKeyboardRemove())
    else:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры.\n'
                                                 'Хочешь еще что-то поменять?',
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user)
        return
