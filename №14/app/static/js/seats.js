// Выбор мест на схеме зала и покупка билетов.
(function () {
  const hall = document.getElementById("hall");
  if (!hall) return;

  const showtimeId = Number(hall.dataset.showtime);
  const maxSeats = Number(hall.dataset.max);
  const summary = document.getElementById("summary");
  const buyButton = document.getElementById("buy");
  const errorBox = document.getElementById("error");

  // Выбранные места: [{row, number, price}, ...]
  const selected = [];

  function formatMoney(value) {
    return value.toLocaleString("ru-RU").replace(/[\u00a0\u202f]/g, " ") + " ₸";
  }

  function seatWord(count) {
    if (count % 10 === 1 && count % 100 !== 11) return "место";
    if ([2, 3, 4].includes(count % 10) && ![12, 13, 14].includes(count % 100)) return "места";
    return "мест";
  }

  function render() {
    if (selected.length === 0) {
      summary.textContent = "Выберите места на схеме";
      buyButton.disabled = true;
      return;
    }
    const total = selected.reduce((sum, seat) => sum + seat.price, 0);
    summary.textContent = `Выбрано ${selected.length} ${seatWord(selected.length)} на сумму ${formatMoney(total)}`;
    buyButton.disabled = false;
  }

  function toggleSeat(button) {
    const seat = {
      row: Number(button.dataset.row),
      number: Number(button.dataset.number),
      price: Number(button.dataset.price),
    };
    errorBox.textContent = "";

    if (button.classList.contains("seat--selected")) {
      button.classList.remove("seat--selected");
      const index = selected.findIndex(s => s.row === seat.row && s.number === seat.number);
      if (index > -1) selected.splice(index, 1);
    } else {
      if (selected.length >= maxSeats) {
        errorBox.textContent = `За один раз можно купить не больше ${maxSeats} билетов`;
        return;
      }
      button.classList.add("seat--selected");
      selected.push(seat);
    }
    render();
  }

  hall.addEventListener("click", (event) => {
    const button = event.target.closest(".seat");
    if (button && !button.disabled) toggleSeat(button);
  });

  buyButton.addEventListener("click", async () => {
    buyButton.disabled = true;
    errorBox.textContent = "";
    try {
      const response = await fetch("/book", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          showtime_id: showtimeId,
          seats: selected.map((s) => [s.row, s.number]),
        }),
      });
      const data = await response.json();
      if (data.ok) {
        window.location.href = data.redirect;
        return;
      }
      errorBox.textContent = data.error || "Не удалось купить билеты";
      if (data.login) {
        errorBox.innerHTML += ` — <a href="${data.login}">войти</a>`;
      }
    } catch (e) {
      errorBox.textContent = "Нет связи с сервером, попробуйте ещё раз";
    }
    buyButton.disabled = false;
  });

  render();
})();
