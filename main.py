import requests
from datetime import date, timedelta
from twilio.rest import Client
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price. 

account_sid = 'AC4514a6c9d783451776071f97e91c838e'
auth_token = '1a9d55e5326497c94b9acfbec7f38203'
NEWS_API_KEY = "417c7c1545d944a6bfa7d73fb64aa39f"
STOCK_API_KEY = "A89QOF6CQYI4Z0IP"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": STOCK_API_KEY,
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()

today_date = date.today()
yesterday = today_date - timedelta(days=1)
yesterday_date_string = yesterday.strftime("%Y-%m-%d")
day_before_yesterday = today_date - timedelta(days=2)
day_before_yesterday_date_string = day_before_yesterday.strftime("%Y-%m-%d")

if yesterday.weekday() == 6 or yesterday.weekday() == 5:
    print("Yesterday the market was close!")
else:
    price_yesterday = float(stock_data["Time Series (Daily)"][yesterday_date_string]["4. close"])
    price_day_before_yesterday = float(stock_data["Time Series (Daily)"][day_before_yesterday_date_string]["4. close"])

    print(stock_data["Time Series (Daily)"][yesterday_date_string]["4. close"])
    print(stock_data["Time Series (Daily)"][day_before_yesterday_date_string]["4. close"])
    print(abs(price_yesterday - price_day_before_yesterday) / price_yesterday * 100)

    if price_yesterday - price_day_before_yesterday > 0:
        trend_indicator = "↗️"
    else:
        trend_indicator = "↘️"

    if abs(price_yesterday - price_day_before_yesterday) / price_yesterday * 100 >= 5:
        news_parameters = {
            "q": COMPANY_NAME,
            "apiKey": NEWS_API_KEY,
            "from": "2024-11-10",
            "to": "2024-11-14",
            "language": "en",
        }
        news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
        news_response.raise_for_status()
        news_data = news_response.json()
        x = slice(3)
        top_3_articles = news_data["articles"][x]
        body = f"Headline: {top_3_articles[0]['title']} \n Brief: {top_3_articles[0]['description']}"
        print(body)

        client = Client(account_sid, auth_token)

        message1 = client.messages.create(
            messaging_service_sid='MGce0dfdb9e1bc9869710eed1b71b0e33d',
            body=COMPANY_NAME + ":" + trend_indicator + "\n" + "Headline: " + top_3_articles[0][
                "title"] + "\n" + "Brief: " + top_3_articles[0]["description"],
            from_='+13617301633',
            to='+4746212148'
        )

        message2 = client.messages.create(
            messaging_service_sid='MGce0dfdb9e1bc9869710eed1b71b0e33d',
            body=COMPANY_NAME + ":" + trend_indicator + "\n" + "Headline: " + top_3_articles[1][
                "title"] + "\n" + "Brief: " + top_3_articles[1]["description"],
            from_='+13617301633',
            to='+4746212148'
        )

        message3 = client.messages.create(
            messaging_service_sid='MGce0dfdb9e1bc9869710eed1b71b0e33d',
            body=COMPANY_NAME + ":" + trend_indicator + "\n" + "Headline: " + top_3_articles[2][
                "title"] + "\n" + "Brief: " + top_3_articles[2]["description"],
            from_='+13617301633',
            to='+4746212148'
        )

## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.


#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
