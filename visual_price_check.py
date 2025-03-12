import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from l2_price_check import get_crypto


print(get_crypto())
data = get_crypto()
price = [float(item["price"]) for item in data]
date_t = [item["formatted_time"].strftime("%d %H:%M") for item in data]


plt.figure(figsize=(20, 10))
plt.plot(date_t, price, marker='o', linestyle='-', color='b', markersize=4)

# Форматирование оси X
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))  # Формат "15:00"
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=150))
# Дополнительные настройки
plt.xticks(rotation=45, ha='right')
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.xlabel("Дата и время", fontsize=12)
plt.ylabel("Цена", fontsize=12)
plt.title("График изменения цены по часам", fontsize=14, pad=20)
plt.tight_layout()

plt.show()