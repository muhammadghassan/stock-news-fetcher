import finnhub
import pandas as pd
from datetime import datetime, timedelta
import time

# Initialize client
finnhub_client = finnhub.Client(api_key="cvvttl9r01qud9qkkie0cvvttl9r01qud9qkkieg")

# === CONFIGURATION ===
symbol = "AMZN"
start_date = datetime(2025, 2, 1)  # earliest date Finnhub allows (1 year ago from today)
end_date = datetime(2025, 4, 16)    # up to today

# Storage
all_news = []

# Daily loop
current = start_date
while current <= end_date:
    date_str = current.strftime('%Y-%m-%d')

    print(f"Fetching news for {symbol} on {date_str}")
    try:
        articles = finnhub_client.company_news(symbol, _from=date_str, to=date_str)

        for item in articles:
            timestamp = item.get("datetime")
            if not timestamp:
                continue
            article_date = datetime.utcfromtimestamp(timestamp).date().strftime("%Y-%m-%d")
            all_news.append({
                "date": article_date,
                "headline": item.get("headline"),
                "summary": item.get("summary"),
                "source": item.get("source"),
                "url": item.get("url"),
                "category": item.get("category"),
                "related": item.get("related"),
                "image": item.get("image")
            })

    except Exception as e:
        print(f"Error on {date_str}: {e}")

    time.sleep(0.4)
    current += timedelta(days=1)

# Convert and save
news_df = pd.DataFrame(all_news)

if not news_df.empty and 'date' in news_df.columns:
    news_df.sort_values(by='date', inplace=True)
    news_df.to_csv(f"{symbol}_news_daily_finnhub.csv", index=False)
    print(f"\n✅ Saved {len(news_df)} articles to {symbol}_news_daily_finnhub.csv")
else:
    print("\n⚠️ No news articles collected.")
