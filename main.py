import requests
import smtplib


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY_STOCK = "37AO3AIXA458V4SF"
API_KEY_NEWS = "3e07ac8d598c4791b0f385f1999018f0"

STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": "IBM",
    "apikey": {API_KEY_STOCK}
}

NEWS_PARAMS = {
    "q": "ibm",
    "from": "2022-12-01",
    "sortBy": "publishedAt",
    "apikey": {API_KEY_NEWS}
}

MY_EMAIL = "mirvaliyevsunnat@gmail.com"
MY_PASSWORD = "bkqkhmxfnsrgvkox"
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
# stock_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey={API_KEY_STOCK}'
response_stock = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMS)
stock_data = response_stock.json()

dic_stock = stock_data["Time Series (Daily)"]
stock_dictionary = [value for (key, value) in dic_stock.items()]
yesterday_closing_price = stock_dictionary[0]['4. close']

# print(stock_dictionary[1])
# print(stock_dictionary[1]['4. close'])

# [new_value for (key, value) in dictionary.items()]
# print(dic_stock)
# new_dictionary = {key: value for (key, value) in dic_stock.items()}
# new_dictionary_s = [(key, value) for key, value in dic_stock.items()]
# print(new_dictionary_s[0])

#TODO 2. - Get the day before yesterday's closing stock price
day_before_yesterday_price = stock_dictionary[1]['4. close']

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = round(abs(float(yesterday_closing_price) - float(day_before_yesterday_price)), 2)

average = round((float(yesterday_closing_price) + float(day_before_yesterday_price))/2, 2)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_diff = round((difference / average) * 100, 2)
print(percentage_diff)

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if percentage_diff > 5:
    print("GET NEWs")

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
response_news = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMS)
news_data = response_news.json()


#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
articles = news_data["articles"][:3]
# print(articles[2])

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
news_dictionary = [(value["title"],value["description"] ) for value in articles]
# print(news_dictionary)

headline = news_dictionary[0][0]
brief = news_dictionary[0][1]
print(headline)
print(brief)




#TODO 9. - Send each article as a separate message via Twilio.
if percentage_diff > 0:
    connection = smtplib.SMTP_SSL("smtp.gmail.com")
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="hayrullamirvaliyev@gmail.com",
            msg=f"Subject:IBM {percentage_diff}%\n\nHeadline: {headline}?\nBrief: {brief}?")
    connection.close()

#Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

