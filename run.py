import feedparser
import pandas as pd
from newspaper import Article
import nltk

for resource in ["tokenizers/punkt", "tokenizers/punkt_tab"]:
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource.split("/")[-1])

rss_feeds = {
    "Reuters": "https://openrss.org/www.reuters.com/world/",
    "Time": "https://time.com/feed/",
    "EuroNews": "https://www.euronews.com/rss",
    "BBC": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "AssociatedPress": "https://feedx.net/rss/ap.xml",
    "NPR_World": "https://feeds.npr.org/1004/rss.xml",
    "NPR_Climate": "https://feeds.npr.org/1167/rss.xml",
    "NPR_Strange": "https://feeds.npr.org/1146/rss.xml",
    "Irish_Examiner": "https://feeds.feedburner.com/ietopstories",
    "The_Journal": "https://www.thejournal.ie/feed/",
    "NYTimes": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "The Verge": "https://www.theverge.com/rss/index.xml"
}

def scrape_news():
    news_items = []

    for source, url in rss_feeds.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            link = entry.link
            print(f"Fetching summary from: {link}")
            summary = ""
            try:
                article = Article(link)
                article.download()
                article.parse()
                article.nlp()
                summary = article.summary
                print(f"✅ Got summary from {source}")
            except Exception as e:
                print(f"❌ Failed to get summary from {link}")
                print(f"Error: {e}")
                summary = "Could not extract summary."

            news_items.append({
                "source": source,
                "title": entry.title,
                "link": link,
                "published": entry.get("published", ""),
                "summary": summary
            })

    df = pd.DataFrame(news_items)
    df.to_csv("news_headlines.csv", index=False)
    print("News with summaries saved.")
    return df

if __name__ == "__main__":
    scrape_news()