from telebot import types
keyboard_start = types.ReplyKeyboardMarkup(True, True)
keyboard_start.row("Регистрация", 'Помощь')


keyboard_back = types.ReplyKeyboardMarkup(True, True)
keyboard_back.row("Назад")


keyboard_types_faculty = types.ReplyKeyboardMarkup(True, True)
keyboard_types_faculty.add(types.KeyboardButton('Назад'))
keyboard_types_faculty.add(types.KeyboardButton('Технический/Естественнонаучный'))
keyboard_types_faculty.add(types.KeyboardButton('Социальный/Гуманитарный'))


keyboard_tech_faculty = types.ReplyKeyboardMarkup(True, True)
keyboard_tech_faculty.add(types.KeyboardButton("Назад"))
keyboard_tech_faculty.add(types.KeyboardButton("МехМат"), types.KeyboardButton("ВМК"), types.KeyboardButton('ФизФак'))
keyboard_tech_faculty.add(types.KeyboardButton("ХимФак"), types.KeyboardButton("БиоФак"),
                          types.KeyboardButton('ФФФХИ'))
keyboard_tech_faculty.add(types.KeyboardButton("Геологический"), types.KeyboardButton("Науки о материалах"))
keyboard_tech_faculty.add(types.KeyboardButton("Почвоведение"), types.KeyboardButton("Биотехнологический"))
keyboard_tech_faculty.add(types.KeyboardButton("ФФМ"), types.KeyboardButton("ФББ"))
keyboard_tech_faculty.add(types.KeyboardButton("Географический"), types.KeyboardButton("ФКИ"))


keyboard_human_faculty = types.ReplyKeyboardMarkup(True, True)
keyboard_human_faculty.add(types.KeyboardButton("Назад"))
keyboard_human_faculty.add(types.KeyboardButton("Филологический"), types.KeyboardButton("Философский"))
keyboard_human_faculty.add(types.KeyboardButton("Журналистский"), types.KeyboardButton("Юридический"))
keyboard_human_faculty.add(types.KeyboardButton("Исторический"), types.KeyboardButton("Гос. управление"))
keyboard_human_faculty.add(types.KeyboardButton("Мировая политика"), types.KeyboardButton("Экономический"))
keyboard_human_faculty.add(types.KeyboardButton("Психологический"), types.KeyboardButton("Социологический"))
keyboard_human_faculty.add(types.KeyboardButton("Политология"), types.KeyboardButton('Искусств'))
keyboard_human_faculty.add(types.KeyboardButton("ФИЯР"), types.KeyboardButton("ВШГА"),
                           types.KeyboardButton('Глобальные процессы'))
keyboard_human_faculty.add(types.KeyboardButton("ИСАА"), types.KeyboardButton("ВШТ"),
                           types.KeyboardButton("ВШКПиУГС"))
keyboard_human_faculty.add(types.KeyboardButton("ВШБ"), types.KeyboardButton("МШЭ"),
                           types.KeyboardButton("ВШССН"))
keyboard_human_faculty.add(types.KeyboardButton("ВШП"), types.KeyboardButton("ВШУИ"))


keyboard_course = types.ReplyKeyboardMarkup(True, True)
keyboard_course.row('Назад')
keyboard_course.row('1', '2')
keyboard_course.row('3', '4')
keyboard_course.row('5', '6')


keyboard_yes_no = types.ReplyKeyboardMarkup(True, True)
keyboard_yes_no.row('Назад')
keyboard_yes_no.row('Да')
keyboard_yes_no.row('Нет')


keyboard_reject_reason = types.ReplyKeyboardMarkup(True, True)
keyboard_reject_reason.row('Несовпадение имени')
keyboard_reject_reason.row('Несовпадение фамилии')
keyboard_reject_reason.row('Несовпадение факультета')
keyboard_reject_reason.row('Несовпадение пола')
keyboard_reject_reason.row('Что это за фото?')


keyboard_search_filter = types.ReplyKeyboardMarkup(True, True)
keyboard_search_filter.row(types.KeyboardButton('Минимальный возраст'), types.KeyboardButton('Максимальный возраст'))
keyboard_search_filter.row(types.KeyboardButton('Пол'), types.KeyboardButton('Факультеты'))
keyboard_search_filter.row(types.KeyboardButton('Минимальный курс'), types.KeyboardButton('Максимальный курс'))
keyboard_search_filter.row(types.KeyboardButton('Авторизованность'))
keyboard_search_filter.row('Искать всех')
keyboard_search_filter.row(types.KeyboardButton('Ничего'))


keyboard_types_faculty_search = types.ReplyKeyboardMarkup(True, True)
keyboard_types_faculty_search.add(types.KeyboardButton('Технический/Естественнонаучный'))
keyboard_types_faculty_search.add(types.KeyboardButton('Социальный/Гуманитарный'))


keyboard_sex = types.ReplyKeyboardMarkup(True, True)
keyboard_sex.row('Назад')
keyboard_sex.row('Парень', "Девушка")


keyboard_tech_faculty_search = types.ReplyKeyboardMarkup(True, True)
keyboard_tech_faculty_search.add(types.KeyboardButton("МехМат"), types.KeyboardButton("ВМК"),
                                 types.KeyboardButton('ФизФак'))
keyboard_tech_faculty_search.add(types.KeyboardButton("ХимФак"), types.KeyboardButton("БиоФак"),
                                 types.KeyboardButton('ФФФХИ'))
keyboard_tech_faculty_search.add(types.KeyboardButton("Геологический"), types.KeyboardButton("Науки о материалах"))
keyboard_tech_faculty_search.add(types.KeyboardButton("Почвоведение"), types.KeyboardButton("Биотехнологический"))
keyboard_tech_faculty_search.add(types.KeyboardButton("ФФМ"), types.KeyboardButton("ФББ"))
keyboard_tech_faculty_search.add(types.KeyboardButton("Географический"), types.KeyboardButton("ФКИ"))


keyboard_human_faculty_search = types.ReplyKeyboardMarkup(True, True)
keyboard_human_faculty_search.add(types.KeyboardButton("Назад"))
keyboard_human_faculty_search.add(types.KeyboardButton("Филологический"), types.KeyboardButton("Философский"))
keyboard_human_faculty_search.add(types.KeyboardButton("Журналистский"), types.KeyboardButton("Юридический"))
keyboard_human_faculty_search.add(types.KeyboardButton("Исторический"), types.KeyboardButton("Гос. управление"))
keyboard_human_faculty_search.add(types.KeyboardButton("Мировая политика"), types.KeyboardButton("Экономический"))
keyboard_human_faculty_search.add(types.KeyboardButton("Психологический"), types.KeyboardButton("Социологический"))
keyboard_human_faculty_search.add(types.KeyboardButton("Политология"), types.KeyboardButton('Искусств'))
keyboard_human_faculty_search.add(types.KeyboardButton("ФИЯР"), types.KeyboardButton("ВШГА"),
                                  types.KeyboardButton('Глобальные процессы'))
keyboard_human_faculty_search.add(types.KeyboardButton("ИСАА"), types.KeyboardButton("ВШТ"),
                                  types.KeyboardButton("ВШКПиУГС"))
keyboard_human_faculty_search.add(types.KeyboardButton("ВШБ"), types.KeyboardButton("МШЭ"),
                                  types.KeyboardButton("ВШССН"))
keyboard_human_faculty_search.add(types.KeyboardButton("ВШП"), types.KeyboardButton("ВШУИ"))


keyboard_yes_no_search = types.ReplyKeyboardMarkup(True, True)
keyboard_yes_no_search.row('Да')
keyboard_yes_no_search.row('Нет')


keyboard_sex_search = types.ReplyKeyboardMarkup(True, True)
keyboard_sex_search.row('Парней')
keyboard_sex_search.row('Девушек')
keyboard_sex_search.row('Всех')


keyboard_change_form = types.ReplyKeyboardMarkup(True, True)
keyboard_change_form.row('Курс', 'Возраст')
keyboard_change_form.row('Фото на анкете', 'Информация на анкете')
keyboard_change_form.row('Ничего')


keyboard_faculty_question = types.ReplyKeyboardMarkup(True, True)
keyboard_faculty_question.row('Добавить факультеты к поиску', 'Убрать факультеты из поиска')
keyboard_faculty_question.row('Добавить все факультеты', 'Убрать все факультеты')
keyboard_faculty_question.row('Ничего')


kb_admin_func_button1 = types.InlineKeyboardButton("Проверка студенческих", callback_data='check_stud')
kb_admin_func_button2 = types.InlineKeyboardButton("Сообщение всем", callback_data='message_to_all')
kb_admin_func_button10 = types.InlineKeyboardButton("Сообщение пользователю", callback_data='message')
kb_admin_func_button3 = types.InlineKeyboardButton("Добавить админа", callback_data='add_admin')
kb_admin_func_button4 = types.InlineKeyboardButton("Удалить админа", callback_data='delete_admin')
kb_admin_func_button5 = types.InlineKeyboardButton("Забанить пользователя", callback_data='ban_user')
kb_admin_func_button6 = types.InlineKeyboardButton("Разбанить пользователя", callback_data='unban_user')
kb_admin_func_button7 = types.InlineKeyboardButton("Включить регистрацию", callback_data='set_on_reg')
kb_admin_func_button8 = types.InlineKeyboardButton("Отключить регистрацию", callback_data='set_off_reg')
kb_admin_func_button9 = types.InlineKeyboardButton("Удалить всех неавторизованных", callback_data='delete_all_not_auth')
keyboard_admin_function = types.InlineKeyboardMarkup()
keyboard_admin_function.add(kb_admin_func_button1)
keyboard_admin_function.row(kb_admin_func_button2, kb_admin_func_button10)
keyboard_admin_function.row(kb_admin_func_button3, kb_admin_func_button4)
keyboard_admin_function.row(kb_admin_func_button5, kb_admin_func_button6)
keyboard_admin_function.row(kb_admin_func_button7, kb_admin_func_button8)
keyboard_admin_function.add(kb_admin_func_button9)


keyboard_settings_not_auth = types.ReplyKeyboardMarkup(True, True)
keyboard_settings_not_auth.row('Назад')
keyboard_settings_not_auth.row('Активировать анкету', 'Деактивировать анкету')
keyboard_settings_not_auth.row('Отправить студенческий на авторизацию')
keyboard_settings_not_auth.row('Удалить свою анкету')


keyboard_settings_auth = types.ReplyKeyboardMarkup(True, True)
keyboard_settings_auth.row('Назад')
keyboard_settings_auth.row('Активировать анкету', 'Деактивировать анкету')
keyboard_settings_auth.row('Удалить свою анкету')


keyboard_course_wtht_back = types.ReplyKeyboardMarkup(True, True)
keyboard_course_wtht_back.row('1', '2')
keyboard_course_wtht_back.row('3', '4')
keyboard_course_wtht_back.row('5', '6')


kb_answer_for_form_btn1 = types.KeyboardButton("Анонимный лайк")
kb_answer_for_form_btn2 = types.KeyboardButton("Открытый лайк")
kb_answer_for_form_btn3 = types.KeyboardButton("Нейтрально")
kb_answer_for_form_btn4 = types.KeyboardButton("Не нравится")
keyboard_answer_for_form = types.ReplyKeyboardMarkup(True, True, row_width=1)
keyboard_answer_for_form.add(kb_answer_for_form_btn1)
keyboard_answer_for_form.add(kb_answer_for_form_btn2)
keyboard_answer_for_form.add(kb_answer_for_form_btn3)
keyboard_answer_for_form.add(kb_answer_for_form_btn4)
