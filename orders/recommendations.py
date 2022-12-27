"""
Stub for recommendations service
Generates random recommendations
"""

import random


class Recommendation:
    BASE = "Купленный препарат необходимо принимать "

    VARIANTS = [
        '1 раз в день',
        '2 раза в день',
        '3 раза в день',
        '5 раз в день',
        '1 раз в два дня',
        '2 раза в неделю',
        'не более одного раза в день',
        'от 2 до 4 раз в день по ощущениям'
    ]

    @staticmethod
    def get_variant():
        return Recommendation.BASE+Recommendation.VARIANTS[random.randint(0, 6)]
