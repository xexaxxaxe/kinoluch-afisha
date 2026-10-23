"""Расчёт цены билета. Все правила и числа — в config.py."""
import config

from ..utils.dates import is_weekend


def seat_price(showtime, row):
    price = config.BASE_PRICE

    if showtime.start.hour < config.MORNING_UNTIL:
        price = price * (100 - config.MORNING_DISCOUNT_PERCENT) // 100

    if is_weekend(showtime.start):
        price = price * (100 + config.WEEKEND_EXTRA_PERCENT) // 100

    if row > showtime.hall.rows - config.VIP_ROWS:
        price += config.VIP_EXTRA

    return price


def row_prices(showtime):
    """Цена места для каждого ряда: {номер ряда: цена}."""
    return {row: seat_price(showtime, row) for row in range(1, showtime.hall.rows + 1)}


def min_price(showtime):
    return min(row_prices(showtime).values())
