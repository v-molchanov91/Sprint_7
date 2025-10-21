BASE_URL = "https://qa-scooter.praktikum-services.ru"

# логин курьера
COURIER_LOGIN = "/api/v1/courier/login"

# создание курьера
COURIER = "/api/v1/courier"

# создание заказа и получение списка заказов
ORDERS = "/api/v1/orders"

# получение заказа по номеру
ORDER_TRACK = "/api/v1/orders/track"

# принять заказ
ACCEPT_ORDER = "/api/v1/orders/accept"


# ошибки курьера
class ErrorCourier:
    MISSING_LOGIN_OR_PASSWORD = "Недостаточно данных для входа"
    IS_NO_ACCOUNT = "Учетная запись не найдена"
    NOT_FOUND = "Not Found."
    NON_EXISTENT_ID = "Курьера с таким id нет."
    MISSING_LOGIN_AND_PASSWORD = "Недостаточно данных для создания учетной записи"
    IS_ALREADY_LOGIN = "Этот логин уже используется. Попробуйте другой."


class ErrorOrder:
    COURIER_NOT_FOUND = "Курьера с таким id не существует"
    ORDER_NOT_FOUND = "Заказа с таким id не существует"
    MISSING_COURIER_OR_ORDER_ID = "Недостаточно данных для поиска"
    NOT_FOUND_ORDER = "Заказ не найден"
