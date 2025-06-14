from phi.tools.yfinance import YFinanceTools
import time
from financial_agent import analyze_stock
import threading
yfinance = YFinanceTools(company_news=True)

# Track last news timestamps
last_news_timestamps = {}
stock_analysis_results = {}

def check_for_news(ticker):
    news = yfinance.company_news(ticker)
    if not news:
        return False

    latest_news = news[0]  # assuming sorted by date
    latest_time = latest_news['datetime']  # format: ISO or Unix timestamp

    last_time = last_news_timestamps.get(ticker)

    if last_time is None or latest_time > last_time:
        last_news_timestamps[ticker] = latest_time
        return True
    return False

def monitor_news_and_analyze(ticker):
    if check_for_news(ticker):
        print(f"New news detected for {ticker}. Running analysis...")
        result = analyze_stock(ticker)
        stock_analysis_results[ticker] = result

def start_news_monitoring(ticker_list, interval=300):
    def loop():
        while True:
            for ticker in ticker_list:
                monitor_news_and_analyze(ticker)
            time.sleep(interval)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()

