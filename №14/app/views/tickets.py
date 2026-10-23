from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from ..auth import current_user, login_required
from ..repositories import orders as orders_repo
from ..repositories import showtimes as showtimes_repo
from ..services import booking

bp = Blueprint("tickets", __name__)


@bp.route("/book", methods=["POST"])
def book():
    if current_user() is None:
        return jsonify({
            "error": "Войдите в аккаунт, чтобы купить билеты",
            "login": url_for("auth.login"),
        }), 401

    data = request.get_json(silent=True) or {}
    st = showtimes_repo.get(data.get("showtime_id"))
    if st is None:
        return jsonify({"error": "Сеанс не найден"}), 404

    try:
        order_id = booking.book(session["user_id"], st, data.get("seats"))
    except booking.BookingError as e:
        return jsonify({"error": str(e)}), 400

    flash(f"Заказ №{order_id} оплачен. Приятного просмотра!")
    return jsonify({"ok": True, "redirect": url_for("tickets.my_tickets")})


@bp.route("/tickets")
@login_required
def my_tickets():
    orders = orders_repo.for_user(session["user_id"])
    items = [
        {"order": o, "left": o.showtime.minutes_left(), "can_cancel": booking.can_cancel(o)}
        for o in orders
    ]
    return render_template("tickets.html", items=items)


@bp.route("/tickets/<int:order_id>/cancel", methods=["POST"])
@login_required
def cancel(order_id):
    try:
        booking.cancel(session["user_id"], order_id)
    except booking.BookingError as e:
        flash(str(e))
    else:
        flash(f"Заказ №{order_id} отменён, деньги вернутся на карту")
    return redirect(url_for("tickets.my_tickets"))
