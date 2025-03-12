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
    massive = {}
    for i in all_serv:
        if i.find(class_='tc-server-inside').text in massive:
            massive[i.find(class_='tc-server-inside').text] += [[i.find(class_='tc-server-inside').text, i.find(class_='tc-amount').text, i.find(class_='tc-price').text.strip()]]
        else:
            massive[i.find(class_='tc-server-inside').text] = [[i.find(class_='tc-server-inside').text,
                                                                i.find(class_='tc-amount').text,
                                                                i.find(class_='tc-price').text.strip()]]
    x = []
    for i, j in massive.items():
        #print(i, len(j))
        x.append([i, len(j)])

    d = sorted(x, key=lambda x: -x[1])
    for i in d:
        print(i)

    # total_amount = sum(amount for amount, price in parsed_data)
    # total_revenue = sum(amount * price for amount, price in parsed_data)
    # weighted_average_price = total_revenue / total_amount

while True:
    main()
    time.sleep(1800)