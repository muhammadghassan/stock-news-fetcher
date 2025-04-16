import requests
import pandas as pd
import finnhub
from datetime import datetime, timedelta
import time

def fetch_finnhub_news(stock_symbol, start_date, end_date, finnhub_api_key):
    finnhub_client = finnhub.Client(api_key=finnhub_api_key)
    all_news = []

    current = start_date
    while current <= end_date:
        date_str = current.strftime('%Y-%m-%d')
        print(f"[Finnhub] Fetching for {stock_symbol} on {date_str}")

        try:
            articles = finnhub_client.company_news(stock_symbol, _from=date_str, to=date_str)
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
                    "related": stock_symbol,
                    "image": item.get("image")
                })
        except Exception as e:
            print(f"Error on {date_str} for {stock_symbol}: {e}")
        time.sleep(0.4)
        current += timedelta(days=1)

    return all_news


def fetch_newsapi_news(company_name, start_date, end_date, newsapi_key):
    base_url = "https://newsapi.org/v2/everything"
    all_articles = []
    current = start_date

    while current <= end_date:
        from_date = current.strftime('%Y-%m-%d')
        to_date = from_date
        print(f"[NewsAPI] Fetching for {company_name} on {from_date}")

        params = {
            "q": company_name,
            "from": from_date,
            "to": to_date,
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": newsapi_key,
            "pageSize": 100,
            "page": 1
        }

        while True:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                if not articles:
                    break

                for article in articles:
                    article_date = article.get("publishedAt", "").split("T")[0]
                    all_articles.append({
                        "date": article_date,
                        "headline": article.get("title"),
                        "summary": article.get("description"),
                        "source": article.get("source", {}).get("name"),
                        "url": article.get("url"),
                        "category": "company news",
                        "related": stock_symbol,
                        "image": None
                    })

                if len(articles) < 100:
                    break
                else:
                    params["page"] += 1
                    time.sleep(1)
            else:
                print(f"NewsAPI error {response.status_code} on {from_date}: {response.text}")
                break

        current += timedelta(days=1)
        time.sleep(1)

    return all_articles


def combined_news_fetcher(company_name, stock_symbol, newsapi_key, finnhub_key):
    today = datetime.today()
    one_month_ago = today - timedelta(days=30)

    # Fetch from both APIs for the last 30 days
    finnhub_news = fetch_finnhub_news(stock_symbol, one_month_ago, today, finnhub_key)
    newsapi_news = fetch_newsapi_news(company_name, one_month_ago, today, newsapi_key)

    # Combine and save
    all_news = finnhub_news + newsapi_news
    df = pd.DataFrame(all_news)
    df.sort_values(by="date", inplace=True)

    filename = f"{stock_symbol}_last30days_combined_news.csv"
    df.to_csv(filename, index=False)
    print(f"\n✅ Saved {len(df)} articles to {filename}")


# ========== USAGE ==========
if __name__ == "__main__":
    company_name = "Tesla Inc"
    stock_symbol = "TSLA"
    newsapi_key = "API KEY"
    finnhub_key = "API KEY"

    combined_news_fetcher(company_name, stock_symbol, newsapi_key, finnhub_key)
