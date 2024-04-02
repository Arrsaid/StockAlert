import requests
import smtplib
import datetime as dt
from secret import *


# parameters for API requests

today = dt.date.today()

parameters_prices = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "META",
    "apikey": API_1
}

parameters_news = {
    'q': "meta",
    "from": today,
    "language": "fr",
    "sortBy": "publishedAt",
    "apikey": API_2
}

url_prices = 'https://www.alphavantage.co/query'
url_news = 'https://newsapi.org/v2/top-headlines'

# get the list of ( date , data) for the stock market

response_prices = requests.get(url_prices, params=parameters_prices)
data_as_list = [(key, value) for (key, value) in response_prices.json()['Time Series (Daily)'].items()]

close_1 = data_as_list[0][1]["4. close"]
close_2 = data_as_list[1][1]["4. close"]

day_1 = data_as_list[0][0]
day_2 = data_as_list[1][0]

if float(close_1) < float(close_2):
    up_down = "DOWN"
elif float(close_1) > float(close_2):
    up_down = "UP"
else:
    up_down = None

p = round(abs(float(close_1) - float(close_2))/float(close_1)*100, 2)


# get the last three news about the stock market
'''
response_news = requests.get(url_news, params=parameters_news)
data_news = response_news.json()

print(data_news)
'''

# creat and send email

text = (f"Dear Said,\n \nI hope this email finds you well."
        f" I wanted to bring to your attention a notable movement  in the "
        f"{parameters_prices["symbol"]} price chart. "
        f"The price is {up_down} {p}% on ({day_1}), the last closing price recorded at {close_1}.\n"
        f"This movement may be of interest to you. "
        f"\n \nBest regards,\n \nYour Python project.")

if p >= 5:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=s_email, password=password)
        connection.sendmail(from_addr=s_email,
                            to_addrs=r_email,
                            msg=f"Subject:Movement in {parameters_prices["symbol"]} Price Chart\n\n" + text)

