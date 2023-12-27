import sender_stand_request
import data


# Функция для изменения значения в параметре firstName в теле запроса
def get_user_body(first_name):
    # Копируется словарь с телом запроса из файла data
    current_body = data.user_body.copy()
    # Изменение значения в поле firstName
    current_body["firstName"] = first_name
    # Возвращается новый словарь с нужным значением firstName
    return current_body


# Функция для позитивной проверки
def positive(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть и он единственный
    assert users_table_response.text.count(str_user) == 1


# Функция негативной проверки, когда в ответе ошибка про символы
def negative(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)

    # В переменную response сохраняется результат
    response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400
    assert response.status_code == 400

    # Проверяется, что в теле ответа атрибут "code" равен 400
    assert response.json()["code"] == 400
    # Проверяется текст в теле ответа в атрибуте "message"
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"


# Функция для негативной проверки, когда в ответе ошибка: "Не все необходимые параметры были переданы"
def negative_pustoy(user_body):
    # В переменную response сохраняется результат
    response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400
    assert response.status_code == 400

    # Проверяется, что в теле ответа атрибут "code" равен 400
    assert response.json()["code"] == 400
    # Проверяется текст в теле ответа в атрибуте "message"
    assert response.json()["message"] == "Не все необходимые параметры были переданы"


# Тест 1. Успешное создание пользователя. Параметр firstName состоит из 2 символов
def test_1():
    positive("Aa")


# Тест 2. Успешное создание пользователя. Параметр firstName состоит из 15 символов
def test_2():
    positive("Ааааааааааааааа")


# Тест 3. Ошибка. Параметр firstName состоит из 1 символа
def test_3():
    negative("A")


# Тест 4. Ошибка. Параметр firstName состоит из 16 символов
def test_4():
    negative("Аааааааааааааааa")


# Тест 5. Успешное создание пользователя. Параметр fisrsName состоит из английских букв
def test_5():
    positive("QWErty")


# Тест 6. Успешное создание пользователя. Параметр firstName состоит из русских букв
def test_6():
    positive("Мария")


# Тест 7. Ошибка. Параметр firstName состоит из слов с пробелами
def test_7():
    negative("Человек и КО")


# Тест 8. Ошибка. Параметр firstName состоит из строки спецсимволов
def test_8():
    negative("\"№%@\",")


# Тест 9. Ошибка. Параметр firstName состоит из строки цифр
def test_9():
    negative("123")


# Тест 10. Ошибка. В запросе нет параметра firstName
def test_10():
    # Копируется словарь с телом запроса из файла data в переменную user_body
    user_body = data.user_body.copy()
    # Удаление параметра firstName из запроса
    user_body.pop("firstName")
    # Проверка полученного ответа
    negative_pustoy(user_body)


# Тест 11. Ошибка. Параметр состоит из пустой строки
def test_11():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_pustoy(user_body)


# Тест 12. Ошибка. Тип параметра firstName: число
def test_12():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(12)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    response = sender_stand_request.post_new_user(user_body)

    # Проверка кода ответа
    assert response.status_code == 400



