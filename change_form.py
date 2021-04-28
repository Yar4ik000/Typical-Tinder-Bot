import registration
from bot import bot
from keyboards import keyboard_change_form
from keyboards import keyboard_course_wtht_back
from telebot import types


def what_change(message, user):
    if message.text == 'Курс':
        sent = bot.send_message(message.chat.id, "Выбери новый курс", reply_markup=keyboard_course_wtht_back)
        bot.register_next_step_handler(sent, change_course, user)
    elif message.text == 'Фото на анкете':
        sent = bot.send_message(message.chat.id, "Отправь новое фото", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(sent, change_photo, user)
    elif message.text == 'Возраст':
        sent = bot.send_message(message.chat.id, "Введи новый возраст", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(sent, change_age, user)
    elif message.text == 'Информация на анкете':
        sent = bot.send_message(message.chat.id, "Введи новую информацию", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(sent, change_info, user)
    elif message.text == 'Ничего':
        bot.send_message(message.chat.id, "Вся информация успешно сохранена", reply_markup=types.ReplyKeyboardRemove())
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, воспользуйся клавиатурой",
                                reply_markup=keyboard_change_form)
        bot.register_next_step_handler(sent, what_change, user)
    print('bababoy')


def change_course(message, user):
    txt = message.text
    if txt != '1' and txt != '2' and txt != '3' and txt != '4' and txt != '5' and txt != '6':
        sent = bot.send_message(message.chat.id, 'Пожалуйста, пользуйся кнопками с клавиатуры',
                                reply_markup=keyboard_course_wtht_back)
        bot.register_next_step_handler(sent, change_course, user)
    else:
        user.course = int(message.text)
        user.save()
        sent = bot.send_message(message.chat.id, "Курс успешно изменен на %d. Хочешь еще что-либо поменять?"
                                % user.course, reply_markup=keyboard_change_form)
        bot.register_next_step_handler(sent, what_change, user)
    print('asfasf')


def change_photo(message, user):
    if not message.photo:
        sent = bot.send_message(message.chat.id, "Кажется это не фото... Попробуй еще раз")
        bot.register_next_step_handler(sent, change_photo, user)
    else:
        user.profile_photo = message.photo[0].file_id
        user.save()
        sent = bot.send_message(message.chat.id, "Фото успешно изменено. Хочешь еще что-либо поменять?",
                                reply_markup=keyboard_change_form)
        bot.register_next_step_handler(sent, what_change, user)
    print('asfaf')


def change_age(message, user):
    if message.text.isdigit():
        if int(message.text) < 15 or int(message.text) > 30:
            sent = bot.send_message(message.chat.id, 'Пожалуйста, введи настойщий возраст')
            bot.register_next_step_handler(sent, change_age, user)
        else:
            user.age = int(message.text)
            user.save()
            sent = bot.send_message(message.chat.id, "Возраст успешно изменен на %d. Хочешь еще что-либо поменять?"
                                    % user.age, reply_markup=keyboard_change_form)
            bot.register_next_step_handler(sent, what_change, user)
    else:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, введи только цифры')
        bot.register_next_step_handler(sent, change_age, user)
    print('asfasf')


def change_info(message, user):
    if len(message.text) > 800:
        sent = bot.send_message(message.chat.id, "Слишком много символов. Попробуй еще раз")
        bot.register_next_step_handler(sent, change_info, user)
        return
    info = message.text
    user.info = info
    user.save()
    sent = bot.send_message(message.chat.id, 'Информация успешно изменена. Хочешь еще что-либо поменять?',
                            reply_markup=keyboard_change_form)
    bot.register_next_step_handler(sent, what_change, user)
    print('asfaf')