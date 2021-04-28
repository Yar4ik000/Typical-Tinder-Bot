from registration import Person
from bot import bot
from bot import ADMIN_ID
import traceback
from peewee import *
from peewee import Expression
from dictionary import faculty_to_FACULTY
from dictionary import faculty_to_number
from dictionary import number_to_faculty
from keyboards import keyboard_answer_for_form
import emoji

db_marks = SqliteDatabase('marks.db')


class Mark(Model):
    mark = CharField(null=True, default=None)
    mark_from = IntegerField(null=True, default=None)
    mark_to = IntegerField(null=True, default=None)

    class Meta:
        database = db_marks


Mark.create_table()


def for_bit_and(user_faculty, person_faculty):
    return Expression(user_faculty, '&', person_faculty)


def start_search(user):
    try:
        if user.srh_all:
            candidates = list(Person.select())
        elif user.srh_sex == 'Любой':
            if user.srh_only_auth:
                candidates = list(Person.select().where((user.srh_min_age <= Person.age <= user.srh_max_age) &
                                                        (user.srh_min_course <= Person.course <= user.srh_max_course) &
                                                        (for_bit_and(user.srh_faculty, Person.faculty) != 0) &
                                                        (Person.is_auth == 1)))
            else:
                candidates = list(Person.select().where((user.srh_min_age <= Person.age <= user.srh_max_age) &
                                                        (user.srh_min_course <= Person.course <= user.srh_max_course) &
                                                        (for_bit_and(user.srh_faculty, Person.faculty) != 0)))
        else:
            if user.srh_only_auth:
                candidates = list(Person.select().where((user.srh_min_age <= Person.age <= user.srh_max_age) &
                                                        (user.srh_min_course <= Person.course <= user.srh_max_course) &
                                                        (for_bit_and(user.srh_faculty, Person.faculty) != 0) &
                                                        (Person.is_auth == 1) &
                                                        (user.srh_sex == Person.sex)))
            else:
                candidates = list(Person.select().where((user.srh_min_age <= Person.age <= user.srh_max_age) &
                                                        (user.srh_min_course <= Person.course <= user.srh_max_course) &
                                                        (for_bit_and(user.srh_faculty, Person.faculty) != 0) &
                                                        (user.srh_sex == Person.sex)))
        index = 0
        if len(candidates) == 0:
            bot.send_message(user.chat_id, 'Не найдено ни одного пользователя с запрашиваемыми характеристиками\n'
                                           'Попробуй поменять фильтр поиска')
            return
        bot.send_message(user.chat_id, "Если анкеты пойдут по второму кругу, попробуй поменять фильтр поиска")
        show_form(user, candidates, index)
        return
    except Exception as e:
        bot.send_message(user.chat_id, "Oops... Что-то пошло не так. Попробуй еще раз заново")
        bot.send_message(ADMIN_ID, 'User_id: %d\n'
                                   'Username: @%s\n'
                                   'Ошибка:\n%s' % (user.chat_id, user.tg, traceback.format_exc()))


def show_form(user, candidates, index):
    try:
        if index >= len(candidates):
            index = 0
        if candidates[index].chat_id == user.chat_id:
            index += 1
            if index >= len(candidates):
                index = 0
            if candidates[index].chat_id == user.chat_id:
                bot.send_message(user.chat_id, 'Не найдено ни одного пользователя с запрашиваемыми характеристиками\n'
                                               'Попробуй поменять фильтр поиска')
                return
        user_mark = Mark.get_or_none(mark_from=user.chat_id, mark_to=candidates[index].chat_id)
        user.id_for_mark = candidates[index].chat_id
        user.save()
        if user_mark:
            if user_mark.mark == 'dislike' or user_mark.mark == 'like':
                index += 1
                if index >= len(candidates):
                    index = 0
            else:
                if candidates[index].is_auth:
                    authorized = emoji.emojize(':white_check_mark:', True) + ' Авторизованный пользователь ' + \
                                 emoji.emojize(':white_check_mark:', True) + '\n'
                else:
                    authorized = emoji.emojize(':x:', True) + ' Неавторизованный пользователь ' + \
                                 emoji.emojize(':x:', True) + '\n'
                bot.send_photo(user.chat_id, candidates[index].profile_photo, authorized +
                               '%s, %d лет, %d курс.\n'
                               '%s\n\n'
                               '%s'
                               % (candidates[index].name, candidates[index].age, candidates[index].course,
                                  faculty_to_FACULTY[number_to_faculty[candidates[index].faculty]], candidates[index].info),
                               reply_markup=keyboard_answer_for_form)
                return
        else:
            if candidates[index].is_auth:
                authorized = emoji.emojize(':white_check_mark:', True) + ' Авторизованный пользователь ' + \
                             emoji.emojize(':white_check_mark:', True) + '\n'
            else:
                authorized = emoji.emojize(':x:', True) + ' Неавторизованный пользователь ' + \
                             emoji.emojize(':x:', True) + '\n'
            bot.send_photo(user.chat_id, candidates[index].profile_photo, authorized +
                           '%s, %d лет, %d курс.\n'
                           '%s\n\n'
                           '%s'
                           % (candidates[index].name, candidates[index].age, candidates[index].course,
                              faculty_to_FACULTY[number_to_faculty[candidates[index].faculty]], candidates[index].info),
                           reply_markup=keyboard_answer_for_form)
            show_form(user, candidates, index)
            print('here')
            return
    except Exception as e:
        bot.send_message(user.chat_id, "Oops... Что-то пошло не так. Попробуй еще раз заново")
        bot.send_message(ADMIN_ID, 'User_id: %d\n'
                                   'Username: @%s\n'
                                   'Ошибка:\n%s' % (user.chat_id, user.tg, traceback.format_exc()))


def anonymous_like(message, user, candidates, index):
    user_for_like = Mark.get_or_none(mark_from=user.id_for_mark, mark_to=user.chat_id)
    if user_for_like is None:
        Mark.create(mark='like', mark_to=user.id_for_mark, mark_from=user.chat_id)
        show_form(user, candidates, index + 1)
        return
    else:
        Mark.create(mark='like', mark_to=user.id_for_mark, mark_from=user.chat_id)
        if user_for_like.mark == 'dislike':
            show_form(user, candidates, index + 1)
            return
        elif user_for_like.mark == 'like':
            user_for_like = candidates[index]
            bot.send_message(user.chat_id, "Ура! У вас совпадение с этим пользователем. Его tg: @%s" %
                             user_for_like.tg)
            bot.send_photo(user.chat_id, user_for_like.profile_photo,
                           '%s, %d лет, %d курс.\n'
                           '%s\n\n'
                           '%s'
                           % (user_for_like.name, user_for_like.age, user_for_like.course,
                              faculty_to_FACULTY[number_to_faculty[user_for_like.faculty]], user_for_like.info))
            bot.send_message(user_for_like.chat_id, "Ура! У вас совпадение с этим пользователем. Его tg: @%s" %
                             user.tg)
            bot.send_photo(user_for_like.chat_id, user.profile_photo,
                           '%s, %d лет, %d курс.\n'
                           '%s\n\n'
                           '%s'
                           % (user.name, user.age, user.course,
                              faculty_to_FACULTY[number_to_faculty[user.faculty]], user.info))
            show_form(user, candidates, index + 1)
            return
