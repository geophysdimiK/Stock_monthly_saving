def download_data():
    finnhub_client = finnhub.Client(api_key=API_KEY)
    stock = 'REBN' #ticker for REBORN Coffee 
    price = finnhub_client.quote('REBN')['c'] #Lists the closing price
    return price
	
def invest(savings_rate):
    weekday = datetime.today().weekday()
    if weekday == 5:  # Saturday
        return
    elif weekday == 6:  # Sunday
        return

    price = download_data()
    
    t = 1 #Transaction fees (in %)
    
    savings_rate *= (1 - t / 100)
    
    shares = savings_rate / price