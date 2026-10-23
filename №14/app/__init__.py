from flask import Flask

import config

from . import auth, db
from .utils import dates, formatting
from .views import schedule, tickets


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["SESSION_COOKIE_NAME"] = config.SESSION_COOKIE_NAME

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(schedule.bp)
    app.register_blueprint(tickets.bp)

    app.add_template_filter(formatting.money, "money")
    app.add_template_filter(formatting.duration, "duration")
    app.add_template_filter(formatting.seats_label, "seats")
    app.add_template_filter(dates.human_day, "day")
    app.add_template_filter(dates.hhmm, "hhmm")
    app.context_processor(auth.inject_user)

    return app
