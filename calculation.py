import finnhub
import pandas as pd
from datetime import datetime
from pandas.tseries.offsets import BDay
import os


API_KEY = "DEIN_FINNHUB_API_KEY"
CSV_FILE = "deposit.csv"

def download_data():
    finnhub_client = finnhub.Client(api_key=API_KEY)
    stock = 'REBN' #ticker for REBORN Coffee 
    price = finnhub_client.quote('REBN')['c'] #Lists the closing price
    return price

def is_first_trading_day():
    today = pd.Timestamp.today().normalize()
    first_day = pd.Timestamp(today.year, today.month, 1)
    first_trading_day = pd.date_range(start=first_day, end=first_day + pd.Timedelta(days=7), freq="B")[0]
    return today == first_trading_day
	
def invest(savings_rate):
    if not is_first_trading_day():
        return "Heute ist nicht der erste Handelstag des Monats."

    price = download_data()
    t = 1 #Transaction fees (in %)
	
    savings_rate_net = savings_rate * (1 - t / 100)
    shares_purchased = savings_rate_net / price


if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        shares_total = df["nr. of shares total"].iloc[-1] + shares_purchased
else:
        shares_total = shares_purchased

value = shares_total * price
now = datetime.now()

new_entry = pd.DataFrame([[now, savings_rate, shares_purchased, shares_total, value]],
                             columns=["datetime", "invested amount", "nr. of shares purchased", "nr. of shares total", "current value"])

new_entry.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)

return f"{shares_purchased:.4f} Aktien zu je {price:.2f} gekauft"
