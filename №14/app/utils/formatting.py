def money(value):
    """12500 -> '12 500 ₸'."""
    return f"{value:,}".replace(",", " ") + " ₸"


def duration(minutes):
    """1565 -> '1 дн. 2 ч 5 мин'."""
    if minutes <= 0:
        return "сеанс уже начался"
    days, rest = divmod(minutes, 24 * 60)
    hours, mins = divmod(rest, 60)
    parts = []
    if days:
        parts.append(f"{days} дн.")
    if hours:
        parts.append(f"{hours} ч")
    parts.append(f"{mins} мин")
    return " ".join(parts)


def seats_label(seats):
    """[(3, 5), (3, 6), (4, 1)] -> 'ряд 3: места 5, 6; ряд 4: место 1'."""
    by_row = {}
    for row, number in sorted(seats):
        by_row.setdefault(row, []).append(number)
    parts = []
    for row, numbers in by_row.items():
        word = "место" if len(numbers) == 1 else "места"
        parts.append(f"ряд {row}: {word} {', '.join(map(str, numbers))}")
    return "; ".join(parts)
