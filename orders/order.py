"""
Class to implement order handling
"""

import random
import json
from constants import PROJECT_ROOT

ORDERS_FILE_PATH = PROJECT_ROOT / 'orders' / 'orders.json'


class Status:
    STATUSES = {
        0: 'Заказ оплачивается',
        1: 'Заказ принят',
        2: 'Сбор заказа',
        3: 'Доставка',
        4: 'Доставлен'
    }
    STATUSES_BACKWARDS = {
        'Заказ оплачивается': 0,
        'Заказ принят': 1,
        'Сбор заказа': 2,
        'Доставка': 3,
        'Доставлен': 4
    }

    def __init__(self):
        self.__status = 0

    def get_status_str(self):
        return Status.STATUSES[self.__status]

    def set_status_by_str(self, status_message: str):
        if status_message in Status.STATUSES_BACKWARDS:
            self.__status = Status.STATUSES_BACKWARDS[status_message]

    def increment_status(self):
        self.__status += 1


class Order:

    def __init__(self, id: int, drug: str, country: str,
                 manufacturer: str, price: str,  status: Status(),
                 address: str, drug_store: str):
        self.id = id
        self.drug = drug
        self.country = country
        self.manufacturer = manufacturer
        self.price = price
        self.status = status
        self.address = address
        self.drug_store = drug_store
        self.waiting_time = str(random.randint(15, 20))+'мин.'


class OrdersManager:
    def __init__(self):
        self.__read_from_json()
        self.orders = {}

    def get_by_id(self, order_id):
        self.__read_from_json()
        return self.orders[order_id]

    def add_new_order(self, order: Order):
        self.__read_from_json()
        order.id = self.__get_unique_order_id()
        self.orders[order.id] = [order.id, order.drug, order.country,
                                 order.manufacturer, order.price,
                                 order.status, order.address,
                                 order.drug_store, order.waiting_time]
        self.__write_to_json()

    def remove_order(self, order_id):
        self.__read_from_json()
        if order_id in self.orders:
            self.orders.pop(order_id)
        self.__write_to_json()

    def __read_from_json(self):
        with open(ORDERS_FILE_PATH, encoding='utf-8', errors='coerce') as orders:
            self.orders = json.load(orders)

    def __write_to_json(self):
        with open(ORDERS_FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(self.orders, file, ensure_ascii=False)

    def __get_unique_order_id(self):
        self.__read_from_json()
        return len(self.orders)+1

    def get_order(self):
        self.__read_from_json()
        return [k for k, v in self.orders.items()][-1]
