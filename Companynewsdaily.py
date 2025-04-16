import requests
import pandas as pd
from datetime import datetime, timedelta
import time

def fetch_daily_news(company_name, start_date_str, api_key):
    base_url = "https://newsapi.org/v2/everything"
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.today()

    all_articles = []

    while start_date <= end_date:
        from_date = start_date.strftime('%Y-%m-%d')
        to_date = from_date  # one day only
        print(f"Fetching news for {company_name} on {from_date}")

        params = {
            "q": company_name,
            "from": from_date,
            "to": to_date,
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": api_key,
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
                    all_articles.append({
                        "date": from_date,
                        "headline": article.get("title"),
                        "summary": article.get("description"),
                        "source": article.get("source", {}).get("name"),
                        "url": article.get("url"),
                        "published_at": article.get("publishedAt", "").split("T")[0],
                    })

                if len(articles) < 100:
                    break
                else:
                    params["page"] += 1
                    time.sleep(1)  # rate limit buffer
            else:
                print(f"Error on {from_date}: {response.status_code}, {response.text}")
                break

        start_date += timedelta(days=1)
        time.sleep(1)  # buffer between days

    # Convert and export
    news_df = pd.DataFrame(all_articles)
    if not news_df.empty:
        news_df["published_at"] = pd.to_datetime(news_df["published_at"])
        news_df.sort_values(by="published_at", inplace=True)
        filename = f"{company_name.replace(' ', '_')}_NewsAPI_from_2025-03-15_to_{end_date.strftime('%Y-%m-%d')}.csv"
        news_df.to_csv(filename, index=False)
        print(f"\n✅ Saved {len(news_df)} articles to {filename}")
    else:
        print("\n⚠️ No articles collected.")

# ========================
# USAGE EXAMPLE
# ========================

api_key = "aa0322608af24eafb23cf99c0ad90df3"
company = "Apple Inc"
start_date = "2025-03-15"

fetch_daily_news(company_name=company, start_date_str=start_date, api_key=api_key)

