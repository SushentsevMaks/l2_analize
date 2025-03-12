import requests
from bs4 import BeautifulSoup
import telebot
import time

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"
url = "https://funpay.com/chips/10/"
chat_id = -695765690

def main():
    try:
        page = requests.get(url)

        soup = BeautifulSoup(page.text, "html.parser")
        all_serv = soup.findAll(class_='tc-server hidden-xxs')
        games = []

        for i in all_serv[1:]:
            games.append(i.text)

        res = list(set(games))

        with open("funpay-games.txt", "r+", encoding="UTF-8") as file:
            d = [i[:-1] for i in file.readlines()]
            for i in res:
                if i not in d:
                    bot = telebot.TeleBot(telega_token)
                    message = "Новый сервак - " + i
                    bot.send_message(chat_id, message)
                    file.write(i + "\n")    
                    time.sleep(5)

    except Exception as e:
        bot.send_message(chat_id, f'Ошибка {e}')

while True:
    main()
    time.sleep(86000)
