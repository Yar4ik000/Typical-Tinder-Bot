from bot import bot
from peewee import *
from telebot import types
from keyboards import keyboard_back
from keyboards import keyboard_types_faculty
from keyboards import keyboard_tech_faculty
from keyboards import keyboard_human_faculty
from keyboards import keyboard_course
from keyboards import keyboard_yes_no
from keyboards import keyboard_yes_no_search
from keyboards import keyboard_sex
from dictionary import faculty_to_number
import search_filter

db = SqliteDatabase('people.db')


class Person(Model):
    profile_photo = CharField(null=True, default=None)
    chat_id = IntegerField(null=True, default=None)
    family = CharField(null=True, default=None)
    name = CharField(null=True, default=None)
    age = IntegerField(null=True, default=None)
    sex = CharField(null=True, default=None)
    course = IntegerField(null=True, default=None)
    faculty = IntegerField(null=True, default=None)
    is_auth = BooleanField(null=True, default=False)
    vision_for_all = BooleanField(null=True, default=True)
    is_active = BooleanField(null=True, default=True)
    is_reg = BooleanField(null=True, default=False)
    tg = CharField(null=True, default=None)
    attempts_to_auth = IntegerField(null=True, default=0)
    info = CharField(null=True, default=None)
    stud_photo = CharField(null=True, default=None)
    is_ban = BooleanField(null=True, default=False)

    # search_settings
    srh_all = BooleanField(null=True, default=True)
    srh_min_age = IntegerField(null=True, default=0)
    srh_max_age = IntegerField(null=True, default=100)
    srh_sex = CharField(null=True, default='Любой')
    srh_min_course = IntegerField(null=True, default=0)
    srh_max_course = IntegerField(null=True, default=10)
    srh_faculty = BigIntegerField(null=True, default=2 ** 37 - 1)
    srh_only_auth = BooleanField(null=True, default=False)

    #id_for_mark = IntegerField(null=True, default=False)

    class Meta:
        database = db


Person.create_table()


def on_registration(id):
    new_user = Person(chat_id=id)
    sent = bot.send_message(id, "Напиши свою фамилию")
    bot.register_next_step_handler(sent, get_family, new_user)


def get_family(message, new_user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, "Пожалуйста, отправь только текст")
        bot.register_next_step_handler(sent, get_family, new_user)
        return
    family = message.text
    new_user.family = family
    new_user.save()
    bot.send_message(message.chat.id, "Твоя фамилия - %s." % family)
    sent = bot.send_message(message.chat.id, "Теперь напиши свое имя.",
                            reply_markup=keyboard_back)
    bot.register_next_step_handler(sent, get_name, new_user)


def get_name(message, new_user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, "Пожалуйста, отправь только текст")
        bot.register_next_step_handler(sent, get_name, new_user)
        return
    elif message.text == 'Назад':
        sent = bot.send_message(message.chat.id, "Напиши свою фамилию")
        bot.register_next_step_handler(sent, get_family, new_user)
        return
    name = message.text
    new_user.name = name
    new_user.save()
    bot.send_message(message.chat.id, "Твоё имя - %s." % name)
    sent = bot.send_message(message.chat.id, "Теперь напиши свой возраст.",
                            reply_markup=keyboard_back)
    bot.register_next_step_handler(sent, get_age, new_user)


def get_age(message, new_user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, "Пожалуйста, отправь только цифры")
        bot.register_next_step_handler(sent, get_age, new_user)
        return
    if message.text == 'Назад':
        sent = bot.send_message(message.chat.id, "Напиши своё имя")
        bot.register_next_step_handler(sent, get_name, new_user)
        return
    elif message.text.isdigit():
        age = int(message.text)
        if age < 15 or age > 30:
            sent = bot.send_message(message.chat.id, 'Пожалуйста, введите настоящий возраст. '
                                                     'Если он и есть настоящий, то значит вы не студент МГУ.',
                                    reply_markup=keyboard_back)
            bot.register_next_step_handler(sent, get_age, new_user)
            return
        else:
            new_user.age = age
            new_user.save()
            bot.send_message(message.chat.id, "Твой возраст - %d." % age)
            sent = bot.send_message(message.chat.id, "Теперь выбери свой пол.",
                                    reply_markup=keyboard_sex)
            bot.register_next_step_handler(sent, get_sex, new_user)
    else:
        sent = bot.send_message(message.chat.id, 'Пожалуйста, введите только цифры.',
                                reply_markup=keyboard_back)
        bot.register_next_step_handler(sent, get_age, new_user)
        return


def get_sex(message, new_user):
    if message.text == 'Парень':
        sex = 'Парень'
        new_user.sex = sex
        new_user.save()
        sent = bot.send_message(message.chat.id, "Ты - %s. Теперь выбери тип своего факультета." % sex,
                                reply_markup=keyboard_types_faculty)
        bot.register_next_step_handler(sent, get_faculty_type, new_user)
    elif message.text == 'Девушка':
        sex = 'Девушка'
        new_user.sex = sex
        new_user.save()
        sent = bot.send_message(message.chat.id, "Ты - %s. Теперь выбери тип своего факультета." % sex,
                                reply_markup=keyboard_types_faculty)
        bot.register_next_step_handler(sent, get_faculty_type, new_user)
    elif message.text == 'Назад':
        sent = bot.send_message(message.chat.id, 'Введи свой возраст')
        bot.register_next_step_handler(sent, get_age, new_user)
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                reply_markup=keyboard_sex)
        bot.register_next_step_handler(sent, get_sex, new_user)
        return


def get_faculty_type(message, new_user):
    if message.text == 'Назад':
        sent = bot.send_message(message.chat.id, "Напиши своё имя")
        bot.register_next_step_handler(sent, get_name, new_user)
        return
    if message.text == 'Технический/Естественнонаучный':
        bot.send_message(message.chat.id, "Твой факультет - %s." % message.text)
        sent = bot.send_message(message.chat.id, "Теперь выбери сам факультет.",
                                reply_markup=keyboard_tech_faculty)
        bot.register_next_step_handler(sent, get_faculty, new_user, 'tech')
    elif message.text == 'Социальный/Гуманитарный':
        bot.send_message(message.chat.id, "Твой факультет - %s." % message.text)
        sent = bot.send_message(message.chat.id, "Теперь выбери сам факультет.",
                                reply_markup=keyboard_human_faculty)
        bot.register_next_step_handler(sent, get_faculty, new_user, 'human')
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                reply_markup=keyboard_types_faculty)
        bot.register_next_step_handler(sent, get_faculty_type, new_user)
        return


def get_faculty(message, new_user, type):
    if message.text is None:
        if type == 'human':
            sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                    reply_markup=keyboard_human_faculty)
            bot.register_next_step_handler(sent, get_faculty, new_user, type)
            return
        else:
            sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                    reply_markup=keyboard_tech_faculty)
            bot.register_next_step_handler(sent, get_faculty, new_user, type)
            return
    if message.text == 'Назад':
        sent = bot.send_message(message.chat.id, "Выбери тип своего факультета", reply_markup=keyboard_types_faculty)
        bot.register_next_step_handler(sent, get_faculty_type, new_user)
        return
    if message.text not in faculty_to_number:
        if type == 'human':
            sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                    reply_markup=keyboard_human_faculty)
            bot.register_next_step_handler(sent, get_faculty, new_user, type)
            return
        else:
            sent = bot.send_message(message.chat.id, "Пожалуйста, используй кнопки с клавиатуры",
                                    reply_markup=keyboard_tech_faculty)
            bot.register_next_step_handler(sent, get_faculty, new_user, type)
            return
    faculty = message.text
    new_user.faculty = faculty_to_number[faculty]
    new_user.save()
    bot.send_message(message.chat.id, "Твой факультет - %s." % faculty)
    sent = bot.send_message(message.chat.id, "Теперь выбери свой курс.",
                            reply_markup=keyboard_course)
    bot.register_next_step_handler(sent, get_course, new_user, type)


def get_course(message, new_user, type):
    if message.text is None:
        sent = bot.send_message(message.chat.id, "Пожалуйста, пользуйся кнопками с клавиатуры",
                                reply_markup=keyboard_course)
        bot.register_next_step_handler(sent, get_course, new_user, type)
        return
    if message.text == 'Назад':
        sent = bot.send_message(message.chat.id, "Выбери свой факультет",
                                reply_markup=keyboard_tech_faculty if type == 'tech' else keyboard_human_faculty)
        bot.register_next_step_handler(sent, get_faculty, new_user, type)
        return
    elif message.text.isdigit():
        course = int(message.text)
        if course < 1 or course > 6:
            sent = bot.send_message(message.chat.id, "Пожалуйста, пользуйся кнопками с клавиатуры",
                                    reply_markup=keyboard_course)
            bot.register_next_step_handler(sent, get_course, new_user, type)
            return
        new_user.course = course
        new_user.save()
        sent = bot.send_message(message.chat.id, "Твой курс - %d. Теперь расскажи что-нибудь о себе, "
                                                 "чтобы другие могли узнать тебя получше. "
                                                 "(Не более 800 символов)" % course,
                                reply_markup=keyboard_back)
        bot.register_next_step_handler(sent, get_some_info, new_user, type)
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, пользуйся кнопками с клавиатуры",
                                reply_markup=keyboard_course)
        bot.register_next_step_handler(sent, get_course, new_user, type)
        return


def get_some_info(message, new_user, type):
    if message.text is None:
        sent = bot.send_message(message.chat.id, "Пожалуйста, отправь только текст",
                                reply_markup=keyboard_back)
        bot.register_next_step_handler(sent, get_some_info, new_user, type)
        return
    if message.text == 'Назад':
        sent = bot.send_message(message.chat.id, "Выбери свой курс", reply_markup=keyboard_course)
        bot.register_next_step_handler(sent, get_course, new_user, type)
        return
    if len(message.text) > 800:
        sent = bot.send_message(message.chat.id, "Слишком много символов. Попробуй еще раз", reply_markup=keyboard_back)
        bot.register_next_step_handler(sent, get_some_info, new_user, type)
        return
    info = message.text
    new_user.info = info
    new_user.save()
    bot.send_message(message.chat.id, "Твоя информация - %s." % info)
    sent = bot.send_message(message.chat.id, "Отправь свое фото, которое будет на анкете",
                            reply_markup=keyboard_back)
    bot.register_next_step_handler(sent, get_profile_photo, new_user, type)


def get_profile_photo(message, new_user, type):
    if message.text == 'Назад':
        sent = bot.send_message(message.chat.id, "Напиши немного информации о себе. "
                                                 "(Не более 800 символов)", reply_markup=keyboard_back)
        bot.register_next_step_handler(sent, get_some_info, new_user, type)
        return
    if not message.photo:
        sent = bot.send_message(message.chat.id, "Кажется это не фото... Попробуй еще раз", reply_markup=keyboard_back)
        bot.register_next_step_handler(sent, get_profile_photo, new_user, type)
        return
    new_user.profile_photo = message.photo[0].file_id
    new_user.save()
    sent = bot.send_message(message.chat.id, "Отлично! А теперь скажи, готов(-а) ли ты пройти сейчас авторизацию?",
                            reply_markup=keyboard_yes_no)
    bot.register_next_step_handler(sent, auth_question, new_user, type)


def auth_question(message, new_user, type):
    if message.text is None:
        sent = bot.send_message(message.chat.id, "Пожалуйста, пользуйся кнопками с клавиатуры",
                                reply_markup=keyboard_yes_no)
        bot.register_next_step_handler(sent, auth_question, new_user, type)
        return
    if message.text == 'Назад':
        sent = bot.send_message(message.chat.id, "Отправь своё фото, которое будет на анкете",
                                reply_markup=keyboard_back)
        bot.register_next_step_handler(sent, get_profile_photo, new_user, type)
        return
    elif message.text == 'Да':
        new_user.tg = message.chat.username
        new_user.is_reg = True
        new_user.save()
        for user in Person.select().where(Person.chat_id == message.chat.id and Person.is_reg == 0):
            user.delete_instance()
        sent = bot.send_message(message.chat.id, "Прекрасно! В таком случае отправь мне фото своего студенческого, "
                                                 "чтобы можно было проверить, что ты из МГУ. Мы нигде не будем "
                                                 "хранить это фото, однако для твоей же безопасности, убедительная "
                                                 "просьба - замажь на фотографии номер своего билета.",
                                reply_markup=keyboard_back)
        bot.register_next_step_handler(sent, auth, new_user, type)
    elif message.text == 'Нет':
        new_user.tg = message.chat.username
        new_user.is_reg = True
        new_user.save()
        for user in Person.select().where(Person.chat_id == message.chat.id and Person.is_reg == 0):
            user.delete_instance()
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, пользуйся кнопками с клавиатуры",
                                reply_markup=keyboard_yes_no)
        bot.register_next_step_handler(sent, auth_question, new_user, type)
        return


def auth(message, new_user, type):
    if message.text == 'Назад':
        sent = bot.send_message(message.chat.id, "Готов ли ты пройти сейчас авторизацию?",
                                reply_markup=keyboard_yes_no)
        bot.register_next_step_handler(sent, auth_question, new_user, type)
        return
    elif not message.photo:
        sent = bot.send_message(message.chat.id, "Кажется это не фото... Попробуй еще раз", reply_markup=keyboard_back)
        bot.register_next_step_handler(sent, auth, new_user, type)
        return
    else:
        new_user.stud_photo = message.photo[0].file_id
        new_user.save()
        sent = bot.send_message(message.chat.id, "Отлично! Длительность подтверждения авторизации займет не более "
                                                 "одного дня. Тебе придет сообщение с результатом проверки. "
                                                 "Хочешь изменить настройки поиска других людей? "
                                                 "(По умолчанию, никаких фильтров нет, то есть тебе будут предлагаться "
                                                 "все доступные анкеты других студентов).",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, go_to_change_search_filter, new_user)


def go_to_change_search_filter(message, user):
    if message.text is None:
        sent = bot.send_message(message.chat.id, "Пожалуйста, пользуйся кнопками с клавиатуры",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, go_to_change_search_filter)
        return
    if message.text == 'Да':
        search_filter.first_change_message(user)
        return
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, "Ты завершил регистрацию", reply_markup=types.ReplyKeyboardRemove())
    else:
        sent = bot.send_message(message.chat.id, "Пожалуйста, пользуйся кнопками с клавиатуры",
                                reply_markup=keyboard_yes_no_search)
        bot.register_next_step_handler(sent, go_to_change_search_filter)
        return
