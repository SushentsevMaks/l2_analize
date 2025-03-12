import requests
from bs4 import BeautifulSoup
import telebot
import time
import pymysql


chat_id = -695765690

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"
url = "https://funpay.com/chips/10/"

def main():
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")
    all_serv = soup.findAll(class_='tc-item')
    massive = []
    for i in all_serv:
        if i.find(class_='tc-server-inside').text == "ElmoreLab.com Harbor x1 (цена за 1к)":
            if len(massive) < 10:
                massive.append([i.find(class_='tc-amount').text, i.find(class_='tc-price').text.strip()])

    parsed_data = []
    for item in massive:
        amount = float(item[0].replace(' кк', '').replace(" ", "").replace(" ", "")) * 1000
        price = float(item[1].replace(' ₽', '').replace(" ", "").replace(" ", ""))
        parsed_data.append((amount, price))

    total_amount = sum(amount for amount, price in parsed_data)
    total_revenue = sum(amount * price for amount, price in parsed_data)
    weighted_average_price = total_revenue / total_amount
    # bot = telebot.TeleBot(telega_token)
    # message = (f"Средневзвешенная цена: {weighted_average_price:.2f} ₽ за единицу\n"
    #            f"Количество: {int(total_amount/1000)}k")
    # bot.send_message(chat_id, message)
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql_req(int(total_amount/1000), weighted_average_price, parsed_data[0][1], formatted_time)

def sql_req(amount: float, price: float, low_price: float, formatted_time):
    try:
        values = (amount, price, low_price, formatted_time)

        try:
            connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
                                             database='l2_check',
                                             cursorclass=pymysql.cursors.DictCursor)
            try:
                with connection.cursor() as cursor:
                    insert_query = "INSERT INTO `harbor` (amount, price, low_price, formatted_time) " \
                                   "VALUES (%s, %s, %s, %s)"
                    cursor.execute(insert_query, (values))
                    connection.commit()
            finally:
                connection.close()

        except Exception as e:
            telebot.TeleBot(telega_token).send_message(chat_id, f"SQL ERROR data fix: {e}\n")

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(chat_id, f"SQL ERROR input attempt: {e}\n")


def get_crypto() -> list:
    try:
        connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
                                             database='l2_check',
                                             cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute("select * from `harbor`")
                result = cursor.fetchall()
        finally:
            connection.close()

        return result

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR get top cripto connect: {e}\n")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1800)