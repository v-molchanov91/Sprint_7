import random
import string
from faker import Faker

fake = Faker("ru_RU")

METRO_STATIONS = list(range(1, 250))


def generate_random_string(length: int = 10) -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_courier_data():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }


def generate_order_data(color: list = None):
    data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.address(),
        "metroStation": random.choice(METRO_STATIONS),
        "phone": fake.phone_number(),
        "rentTime": random.randint(1, 7),
        "deliveryDate": (fake.future_date(end_date="+30d")).strftime("%Y-%m-%d"),
        "comment": fake.sentence(nb_words=6),
    }
    if color is not None:
        data["color"] = color
    return data
