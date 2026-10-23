from datetime import date, datetime, timedelta

WEEKDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
MONTHS = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
]


def is_weekend(day):
    """Суббота или воскресенье."""
    return day.isoweekday() >= 6


def human_day(day):
    """date или datetime -> 'пт, 23 октября'."""
    return f"{WEEKDAYS[day.weekday()]}, {day.day} {MONTHS[day.month - 1]}"


def hhmm(moment):
    return moment.strftime("%H:%M")


def next_days(count):
    today = date.today()
    return [today + timedelta(days=i) for i in range(count)]


def parse_day(text, default):
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return default
