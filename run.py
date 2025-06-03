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
    "CNN": "http://rss.cnn.com/rss/cnn_topstories.rss",
    "NPR": "http://www.npr.org/rss/rss.php?id=1001",
    "Irish_Examiner": "https://feeds.feedburner.com/ietopstories",
    "NYTimes": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "The Verge": "https://www.theverge.com/rss/index.xml"
}

def scrape_news():
    news_items = []

    for source, url in rss_feeds.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
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