# 📈 Stock News Fetcher (Finnhub + NewsAPI)

This project provides scripts to collect and analyze daily stock-related news from two APIs: **Finnhub** and **NewsAPI**. You can fetch historical news from:

- 📊 **Finnhub** – up to **1 year of historical data**
- 📰 **NewsAPI** – up to **30 days of historical data**

Three scripts are provided for modular and combined use cases.

---

## 🔧 Files and Their Functionality

### `comstock.py` ✅
**Purpose**: Combines both NewsAPI and Finnhub to retrieve news from the last 30 days for a specified stock.

- Input: `company_name`, `stock_symbol`, API keys
- Output: CSV file with combined news (`{stock_symbol}_last30days_combined_news.csv`)
- Columns: `date`, `headline`, `summary`, `source`, `url`, `category`, `related`, `image`
- Ideal for: Most accurate recent coverage from both sources

---

### `STOCKnewsdaily.py`
**Purpose**: Uses the Finnhub API to fetch daily news by **stock symbol** for a date range (up to 1 year back).

- Input: set `symbol`, `start_date`, `end_date` in code
- Output: `{symbol}_news_daily_finnhub.csv`
- Ideal for: Deeper historical datasets

---

### `Companynewsdaily.py`
**Purpose**: Uses NewsAPI to fetch articles by **company name** (limited to past 30 days).

- Input: set `company_name`, `start_date`, and `newsapi_key` in code
- Output: `{company_name}_NewsAPI_from_{start_date}_to_{today}.csv`
- Ideal for: Broader, real-time headlines on popular company names

---

## 🔐 API Rate Limits

### Finnhub
- Free Tier Limit: **60 API calls/min**
- Hard Limit: **30 API calls/second**
- Historical Access: **1 year back**
- Endpoint used: `/company-news`

[→ Finnhub Docs](https://finnhub.io/docs/api/company-news)

### NewsAPI
- Free Tier Limit: **1000 requests/day**
- Historical Access: **30 days max**
- Endpoint used: `/v2/everything`

[→ NewsAPI Docs](https://newsapi.org/docs/endpoints/everything)

---

## ✅ Requirements

Install dependencies:

```bash
pip install pandas requests finnhub-python
```
## 🚀 Usage Examples
Run combined fetcher for Tesla:
```bash
python comstock.py
```
(You can edit company_name, stock_symbol, and keys directly in the script.)

## 📥 Output Structure
CSV outputs contain the following standardized fields:
date	headline	summary	source	url	category	related	image
2025-04-15	Tesla hits record profits	Summary ...	Bloomberg	http://...	company news	TSLA	http://...

