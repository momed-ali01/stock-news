import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "L8NSPMRVJH42MRG6"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "17ba26d3879b4ffda64409edf5b590cf"
TWILIO_ACCOUNT_SID = "AC935638423523477086d6ca2fc803f00e"
TWILIO_AUTH_TOKEN = "14705bf691130b3b1b7259868df570da"

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [
# new_value for (key, value) in dictionary.items()]
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY

}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint:
# https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "🔼"
else:
    up_down = "🔽"


# Work out the percentage difference in price between closing price yesterday and closing price the day before
# yesterday.
diff_percent = round((difference / float(yesterday_closing_price)) * 100)

# If percentage is greater than 5 then print("Get News").
if abs(diff_percent) > 5:
    print("Gettin' News")
    # Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_params = {
        "q": COMPANY_NAME,
    }
    news_headers = {
        "X-Api-Key": NEWS_API_KEY
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params, headers=news_headers)
    articles = news_response.json()["articles"]

    # Use Python slice operator to create a list that contains the first 3 articles.
    # Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]
    # STEP 3: Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    # TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles =[f"{STOCK_NAME}: {up_down}{diff_percent}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)

    # TODO 9. - Send each article as a separate message via Twilio.
    for article in formatted_articles:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_='+12083143160',
            to='+252638114350',
            body=article
        )

# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
