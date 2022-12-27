import random

PLACES = [
    'Большая Печерская',
    'Белинского',
    'Максима Горького',
    'Ванеева',
    'Фруктовая'
]


class AddressGenerator:
    def get_place(self):
        return PLACES[random.randint(0, len(PLACES)-1)]+', '+str(random.randint(1, 150))
