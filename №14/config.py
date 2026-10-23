import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = "urok-4-kino-secret-key"
SESSION_COOKIE_NAME = "kino_student"
DATABASE = os.path.join(BASE_DIR, "kino.db")
PORT = 5000

# Сколько дней вперёд показывать афишу
DAYS_AHEAD = 7

# ---------- Цены ----------
BASE_PRICE = 2000                # обычный билет, ₸
MORNING_UNTIL = 12               # сеансы, которые начинаются раньше 12:00, — утренние
MORNING_DISCOUNT_PERCENT = 30    # скидка на утренние сеансы
WEEKEND_EXTRA_PERCENT = 20       # наценка в субботу и воскресенье
VIP_ROWS = 2                     # сколько последних рядов в каждом зале — VIP
VIP_EXTRA = 500                  # доплата за VIP-место, ₸

# ---------- Покупка и возврат ----------
MAX_SEATS = 6                    # максимум билетов в одном заказе
CANCEL_MINUTES = 60              # вернуть билет можно не позже чем за столько минут до начала
