from bot import bot
from keyboards import keyboard_settings_auth
from keyboards import keyboard_settings_not_auth
from keyboards import keyboard_yes_no_search
from telebot import types


def choose_settings(message, user, is_auth):
    if message.text is None:
        sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                reply_markup=keyboard_settings_auth if is_auth else keyboard_settings_not_auth)
        bot.register_next_step_handler(sent, choose_settings, user, is_auth)
        return
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Ничего не меняем', reply_markup=types.ReplyKeyboardRemove())
        return
    elif message.text == 'Активировать анкету':
        if user.is_active:
            sent = bot.send_message(message.chat.id, "Твоя анкета уже активирована. Хочешь еще что-то поменять?",
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user, is_auth)
            return
        else:
            user.is_active = True
            user.save()
            sent = bot.send_message(message.chat.id, "Теперь твоя анкета активирована. "
                                                     "Хочешь еще что-то поменять?",
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user, is_auth)
            return
    elif message.text == 'Деактивировать анкету':
        if not user.is_active:
            sent = bot.send_message(message.chat.id, "Твоя анкета уже деактивирована. Хочешь еще что-то поменять?",
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user, is_auth)
            return
        else:
            user.is_active = False
            user.save()
            sent = bot.send_message(message.chat.id, "Теперь твоя анкета деактивирована. "
                                                     "Хочешь еще что-то поменять?",
                                    reply_markup=keyboard_yes_no_search)
            bot.register_next_step_handler(sent, change_more, user, is_auth)
            return
    elif message.text == 'Удалить свою анкету':
        sent = bot.send_message(message.chat.id, "Ты уверен(-а) в своём выборе? Вся информация о тебе будет "
                                                 "удалена, и если ты захочешь вернуться, придется заново "
                                                 "проходить регистрацию" + ' и авторизацию.' if is_auth else '.',
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, delete_account_question, user, is_auth)
        return
    elif is_auth:
        sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                reply_markup=keyboard_settings_auth if is_auth else keyboard_settings_not_auth)
        bot.register_next_step_handler(sent, choose_settings, user, is_auth)
        return
    else:
        if message.text == 'Отправить студенческий на авторизацию':
            if user.stud_photo != 'REJECT' and user.stud_photo != 'OK':
                sent = bot.send_message(message.chat.id, 'Ты уже отправил фото на проверку. '
                                                         'Хочешь еще что-то поменять?',
                                        reply_markup=keyboard_yes_no_search)
                bot.register_next_step_handler(sent, change_more, user, is_auth)
                return
            else:
                sent = bot.send_message(message.chat.id, "Отправь фото студенческого. По возможности, "
                                                         "замажь номер билета.",
                                        reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(sent, auth, user, is_auth)
                return
        else:
            sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                    reply_markup=keyboard_settings_auth if is_auth else keyboard_settings_not_auth)
            bot.register_next_step_handler(sent, choose_settings, user, is_auth)
            return


def change_more(message, user, is_auth):
    if message.text is None:
        sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user, is_auth)
        return
    elif message.text == 'Да':
        sent = bot.send_message(message.chat.id, 'Выбери раздел настроек',
                                reply_markup=keyboard_settings_auth if user.is_auth else keyboard_settings_not_auth)
        bot.register_next_step_handler(sent, choose_settings, user, user.is_auth)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Все изменения сохранены', reply_markup=types.ReplyKeyboardRemove())
        return
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user, is_auth)
        return


def delete_account_question(message, user, is_auth):
    if message.text is None:
        sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, delete_account_question, user)
        return
    elif message.text == 'Да':
        user.delete_instance()
        bot.send_message(message.chat.id, 'Твоя анкета была удалена', reply_markup=types.ReplyKeyboardRemove())
        return
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Все изменения сохранены', reply_markup=types.ReplyKeyboardRemove())
        return
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, delete_account_question, user, is_auth)
        return



def auth(message, user, is_auth):
    if not message.photo:
        sent = bot.send_message(message.chat.id, "Кажется это не фото... Попробуй еще раз")
        bot.register_next_step_handler(sent, auth, user)
        return
    else:
        user.stud_photo = message.photo[0].file_id
        user.save()
        sent = bot.send_message(message.chat.id, "Фото успешно отправлено на проверку. Длительность проверки "
                                                 "не больше одного дня.\nХочешь еще что-то поменять?",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, change_more, user, is_auth)
