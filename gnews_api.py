import requests
import pandas as pd
from datetime import datetime, timedelta


def fetch_news(start_date, end_date, api_key):
    """
    Fetch news articles from the GNews API for a specific date range and keywords.
    """
    base_url = "https://gnews.io/api/v4/search"
    country = "au"  # Filter for Australia
    query = " "  # Add Search terms here

    # Ensure the dates follow the required format 'YYYY-MM-DDThh:mm:ssZ'
    start_date = start_date + "T00:00:00Z"
    end_date = end_date + "T23:59:59Z"

    params = {
        "q": query,
        "country": country,
        "from": start_date,
        "to": end_date,
        "max": 100,  # Maximum results per request
        "apikey": api_key
    }

    # Send the request
    response = requests.get(base_url, params=params)
    print(f"Request URL: {response.url}")  # Log the full request URL for debugging

    if response.status_code == 200:
        try:
            return response.json()
        except Exception as e:
            print(f"Error decoding JSON response: {e}")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def extract_articles(data):
    """
    Extract relevant fields from the API response.
    """
    if data and "articles" in data:
        articles = data["articles"]
        return [{
            "Title": article.get("title", ""),
            "Description": article.get("description", ""),
            "URL": article.get("url", ""),
            "PublishedAt": article.get("publishedAt", ""),
            "Source": article.get("source", {}).get("name", "")
        } for article in articles]
    else:
        print("No articles found.")
        return []


def save_to_excel(articles, filename):
    """
    Save extracted articles to an Excel file.
    """
    df = pd.DataFrame(articles)
    if not df.empty:
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save. Skipping file creation.")


def fetch_news_for_month(year, month, api_key):
    """
    Fetch news articles for a specific month and year.
    """
    # Calculate the start and end dates for the specified month
    start_date = datetime(year, month, 1)
    next_month = start_date + timedelta(days=31)
    next_month = next_month.replace(day=1)
    end_date = next_month - timedelta(days=1)

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    print(f"Fetching news for {start_date_str} to {end_date_str}")

    # Fetch and process data
    data = fetch_news(start_date_str, end_date_str, api_key)
    articles = extract_articles(data)

    # Save the results to an Excel file
    month_name = start_date.strftime('%B_%Y')
    save_to_excel(articles, f"Australia_News_{month_name}.xlsx")


def main():
    api_key = "96f32b02e5733c97fbe7d734017e67cf"  # Replace with your GNews API key
    year =   ''# Specify the year
    month =    '' # Specify the month (1 = January, 12 = December)

    # Fetch and save data for the specified month
    fetch_news_for_month(year, month, api_key)


if __name__ == "__main__":
    main()
