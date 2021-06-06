import telebot
import aiogram
from peewee import *
import traceback
from keyboards import keyboard_start
from keyboards import keyboard_yes_no_search
from keyboards import keyboard_change_form
from keyboards import keyboard_search_filter
from keyboards import keyboard_settings_auth
from keyboards import keyboard_settings_not_auth
from bot import bot
from bot import ADMIN_ID
import registration
import admins
import change_form
import search_filter
from dictionary import faculty_to_FACULTY
from dictionary import number_to_faculty
import hashlib
import emoji
import setting
import search




@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Привет! Я - бот знакомств. Хоть изначально я '
                     'планировался для использования только ребятами из МГУ, '
                     'сейчас же мной может пользоваться кто угодно. '
                     'Однако есть небольшие ограничения. Например, '
                     'твою анкету будут видеть все желающие, а также, '
                     'если проверенный пользователь выберет специальную опцию, '
                     'то его анкета не будет тебе предлагаться. Ты можешь снять их, '
                     'если пройдешь идентификацию. Для этого нужно будет отправить фото '
                     'студенческого билета. Но сначала тебе нужно пройти '
                     'регистрацию. Для этого нажми соответствующую кнопку на клавиатуре. '
                     'Если есть вопросы, нажми на кнопку "Помощь".', reply_markup=keyboard_start)
    bot.register_next_step_handler(message, first_answer)


def first_answer(message):
    if message.text is None:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры')
        bot.register_next_step_handler(sent, first_answer)
        return
    if message.text == 'Регистрация':
        check_reg = admins.Admin.get(admin_id=ADMIN_ID)
        if not check_reg.reg_on:
            bot.send_message(message.chat.id, "Прости, прямо сейчас регистрация отключена. Попробуй через пару минут",
                             reply_markup=telebot.types.ReplyKeyboardRemove())
            return
        check_reg = registration.Person.get_or_none(chat_id=message.chat.id)
        if check_reg is not None:
            if check_reg.is_reg:
                bot.send_message(message.chat.id, "Прости, ты уже зарегестрирован(-а). "
                                                  "Но ты в любой момент можешь поменять "
                                                  "что-либо в информации о себе в настройках анкеты.",
                                 reply_markup=telebot.types.ReplyKeyboardRemove())
                return
        bot.send_message(message.chat.id, "Мы автоматически получим твой username телеграмма. Именно он "
                                          "будет выводится тому, с кем у тебя будет match. Если хочешь "
                                          "указать какие то отдельные соц сети, то можешь потом написать "
                                          "их в информации о себе.")
        bot.send_message(message.chat.id, "Будь внимателен(-на)! После окончания регистрации ты сможешь поменять "
                                          "только возраст, фото, информацию и курс.")
        registration.on_registration(message.chat.id)
    elif message.text == 'Помощь':
        help_message(message)
        return
    else:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры')
        bot.register_next_step_handler(sent, first_answer)
        return


@bot.message_handler(commands=['admin'])
def check_admin_command(message):
    admins.check_admin(message)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "/start - начало работы\n"
                                      "/help - получить эту информацию\n"
                                      "/search_filter - изменить настройки поиска\n"
                                      "/search - начать поиск\n"
                                      "/settings - настройки вашего аккаунта\n"
                                      "/form - ваша анкета\n"
                                      "/support_creator - поддержать материально создателя")


@bot.message_handler(commands=['form'])
def view_and_change_my_form(message):
    user = registration.Person.get_or_none(chat_id=message.chat.id)
    if not user:
        check_ban = admins.BanUser.get_or_none(banned_user_id=message.chat.id)
        if check_ban:
            bot.send_message(message.chat.id, 'Ты забанен')
            return
        bot.send_message(message.chat.id, "Сначала тебе надо пройти регистрацию")
        return
    else:
        if user.is_ban:
            bot.send_message(message.chat.id, 'Ты забанен')
            return
        check_ban = admins.BanUser.get_or_none(banned_user_id=message.chat.id)
        if check_ban:
            bot.send_message(message.chat.id, 'Ты забанен')
            return
        bot.send_message(message.chat.id, 'Вот так выглядит твоя анкета')
        if user.is_auth:
            authorized = emoji.emojize(':white_check_mark:', True) + ' Авторизованный пользователь ' + \
                         emoji.emojize(':white_check_mark:', True) + '\n'
        else:
            authorized = emoji.emojize(':x:', True) + ' Неавторизованный пользователь ' + \
                         emoji.emojize(':x:', True) + '\n'
        bot.send_photo(message.chat.id, user.profile_photo, authorized +
                       '%s, %d лет, %d курс.\n'
                       '%s\n\n'
                       '%s'
                       % (user.name, user.age, user.course, faculty_to_FACULTY[number_to_faculty[user.faculty]],
                          user.info))
        sent = bot.send_message(message.chat.id, "Хочешь что-либо изменить?", reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_form_main, user)


def change_form_main(message, user):
    if message.text == 'Нет':
        bot.send_message(message.chat.id, 'Хорошо, ничего не меняем', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == 'Да':
        sent = bot.send_message(message.chat.id, 'Выбери что хочешь поменять', reply_markup=keyboard_change_form)
        bot.register_next_step_handler(sent, change_form.what_change, user)
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, пользуйся кнопками с клавиатуры. Хочешь что-либо "
                                                 "изменить?", reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_form_main, user)


@bot.message_handler(commands=['search_filter'])
def view_and_change_search_filter(message):
    user = registration.Person.get_or_none(registration.Person.chat_id == message.chat.id)
    if not user:
        check_ban = admins.BanUser.get_or_none(banned_user_id=message.chat.id)
        if check_ban:
            bot.send_message(message.chat.id, 'Ты забанен')
            return
        bot.send_message(message.chat.id, "Сначала тебе надо пройти регистрацию")
        return
    if user.is_ban:
        bot.send_message(message.chat.id, 'Ты забанен')
        return
    check_ban = admins.BanUser.get_or_none(banned_user_id=message.chat.id)
    if check_ban:
        bot.send_message(message.chat.id, 'Ты забанен')
        return
    faculty_str = ''
    if user.srh_faculty == 2 ** 37 - 1:
        faculty_str = 'все'
    else:
        for i in range(36):
            if user.srh_faculty & (2 ** i) != 0:
                faculty_str += number_to_faculty[2 ** i] + '\n'
        if faculty_str == '':
            faculty_str = 'ни одного не выбрано'
    if not user:
        bot.send_message(message.chat.id, "Сначала тебе надо пройти регистрацию")
    else:
        if user.srh_all:
            bot.send_message(message.chat.id, "Ты ищешь любых пользователей")
            sent = bot.send_message(message.chat.id, 'Хочешь поменять что-то?', reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_search_filter, user)
            return
        bot.send_message(message.chat.id, "Твои настройки поиска:\n"
                                          "Возраст: %d-%d\n"
                                          "Курс: %d-%d\n"
                                          "Пол: %s\n"
                                          "Искать: %s\n"
                                          "Факультеты: \n%s"
                         % (user.srh_min_age, user.srh_max_age, user.srh_min_course, user.srh_max_course,
                            user.srh_sex, 'Только авторизованных пользователей' if user.srh_only_auth
                            else 'Всех пользователей', faculty_str))
        sent = bot.send_message(message.chat.id, 'Хочешь поменять что-то?', reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_search_filter, user)


def change_search_filter(message, user):
    if message.text == 'Нет':
        bot.send_message(message.chat.id, 'Хорошо, ничего не меняем', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == 'Да':
        sent = bot.send_message(message.chat.id, 'Выбери что хочешь поменять', reply_markup=keyboard_search_filter)
        bot.register_next_step_handler(sent, search_filter.choose_filter_field, user)
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, пользуйся кнопками с клавиатуры. Хочешь что-либо "
                                                 "изменить?", reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_search_filter, user)


@bot.message_handler(commands=['settings'])
def settings(message):
    user = registration.Person.get_or_none(registration.Person.chat_id == message.chat.id)
    if not user:
        check_ban = admins.BanUser.get_or_none(banned_user_id=message.chat.id)
        if check_ban:
            bot.send_message(message.chat.id, 'Ты забанен')
            return
        bot.send_message(message.chat.id, "Сначала тебе надо пройти регистрацию")
        return
    if user.is_ban:
        bot.send_message(message.chat.id, 'Ты забанен')
        return
    check_ban = admins.BanUser.get_or_none(banned_user_id=message.chat.id)
    if check_ban:
        bot.send_message(message.chat.id, 'Ты забанен')
        return
    sent = bot.send_message(message.chat.id, 'Выбери раздел настроек',
                            reply_markup=keyboard_settings_auth if user.is_auth else keyboard_settings_not_auth)
    bot.register_next_step_handler(sent, setting.choose_settings, user, user.is_auth)
    return


@bot.message_handler(commands=['support_creator'])
def help_message(message):
    try:
        print (1 / 0)
        bot.send_message(message.chat.id, "Буду благодарен за любую вашу поддержку!\n"
                                          "Сбер - 4276160484902045\n"
                                          "Тинькоф - ...")
        return
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка:\n%s" % traceback.format_exc())


@bot.message_handler(commands=['search'])
def go_to_search(message):
    try:
        user = registration.Person.get_or_none(chat_id=message.chat.id)
        if user is None:
            bot.send_message(message.chat.id, 'Сначала тебе нужно зарегестрироваться')
            return
        bot.send_message(message.chat.id, "Начинаем поиск...")
        search.start_search(user)
        return
    except Exception as e:
        bot.send_message(message.chat.id, "Oops... Что-то пошло не так. Попробуй еще раз заново")
        bot.send_message(ADMIN_ID, 'User_id: %d\n'
                                   'Username: @%s\n'
                                   'Ошибка:\n%s' % (message.chat.id, 'qwe', traceback.format_exc()))


bot.polling()
