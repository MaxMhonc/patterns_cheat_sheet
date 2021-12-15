import json
from decimal import Decimal

text = '{"total": 9.61, "items": ["Americano", "Omelet"]}'


def build_decimal(string):
    return Decimal(string)


print(json.loads(text, parse_float=build_decimal))
