from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import config

from ..repositories import showtimes as showtimes_repo
from ..services import pricing
from ..utils import dates

bp = Blueprint("schedule", __name__)


@bp.route("/")
def index():
    days = dates.next_days(config.DAYS_AHEAD)
    day = dates.parse_day(request.args.get("day"), date.today())
    if day not in days:
        day = days[0]

    movies = {}
    for st in showtimes_repo.for_day(day):
        if st.is_past():
            continue
        free = st.hall.capacity - showtimes_repo.count_taken(st.id)
        entry = movies.setdefault(st.movie.id, {"movie": st.movie, "showtimes": []})
        entry["showtimes"].append({
            "showtime": st,
            "free": free,
            "price": pricing.min_price(st),
        })
    for entry in movies.values():
        entry["showtimes"].sort(key=lambda item: item["showtime"].start)

    return render_template("schedule.html", days=days, day=day, movies=list(movies.values()))


@bp.route("/showtime/<int:showtime_id>")
def showtime(showtime_id):
    st = showtimes_repo.get(showtime_id)
    if st is None:
        abort(404)
    if st.is_past():
        flash("Этот сеанс уже начался — выберите другой")
        return redirect(url_for("schedule.index"))

    return render_template(
        "showtime.html",
        st=st,
        taken=showtimes_repo.taken_seats(st.id),
        prices=pricing.row_prices(st),
        max_seats=config.MAX_SEATS,
    )
