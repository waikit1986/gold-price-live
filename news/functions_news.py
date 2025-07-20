import sys
import os
from datetime import datetime
from typing import Dict, List

import httpx
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from news.schema_news import (
    NewsArticleSchema,
    NewsTopicToSave,
    NewsTickerSentimentToSave,
    NewsArticleToSave,
)
from news.models_news import NewsArticle, NewsTopic, NewsTickerSentiment
from db.database import SessionLocal

def download_news_articles() -> List[NewsArticleToSave]:
    url = (
        "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=economy&economy_macro,monetary,economy_fiscal&limit=300&sort=LATEST&apikey=N7XFFLQ444WX8GAT"
    )

    articles = []

    with httpx.Client() as client:
        response = client.get(url)

    if response.status_code == 200:
        data = response.json()
        feed = data.get("feed", [])

        for article in feed:
            try:
                article_obj = NewsArticleToSave(
                    title=article.get("title", ""),
                    url=article.get("url"),
                    time_published=datetime.strptime(article["time_published"], "%Y%m%dT%H%M%S"),
                    author=", ".join(article.get("authors", [])),
                    summary=article.get("summary", ""),
                    banner_image=article.get("banner_image", ""),
                    source=article.get("source", ""),
                    category_within_source=article.get("category_within_source", ""),
                    source_domain=article.get("source_domain", ""),
                    overall_sentiment_score=float(article.get("overall_sentiment_score", 0.0)),
                    overall_sentiment_label=article.get("overall_sentiment_label", ""),
                    topics=[
                        NewsTopicToSave(
                            topic=t["topic"],
                            relevance_score=float(t["relevance_score"])
                        )
                        for t in article.get("topics", [])
                    ],
                    ticker_sentiment=[
                        NewsTickerSentimentToSave(
                            ticker=t["ticker"],
                            relevance_score=float(t["relevance_score"]),
                            ticker_sentiment_score=float(t["ticker_sentiment_score"]),
                            ticker_sentiment_label=t["ticker_sentiment_label"]
                        )
                        for t in article.get("ticker_sentiment", [])
                    ]
                )
                articles.append(article_obj)
                save_articles_to_db([article_obj])
            except Exception as e:
                print(f"Error processing article: {e}")
    else:
        print(f"Failed to fetch articles: {response.status_code}")

    return articles

def save_articles_to_db(articles: List[NewsArticleToSave]):
    session: Session = SessionLocal()
    try:
        for article in articles:
            existing = session.query(NewsArticle).filter_by(url=str(article.url)).first()
            if existing:
                print(f"Duplicate found: {article.title}")
                continue

            db_article = NewsArticle(
                id=article.id,
                title=article.title,
                url=str(article.url),
                time_published=article.time_published,
                author=article.author,
                summary=article.summary,
                banner_image=str(article.banner_image) if article.banner_image else None,
                source=article.source,
                category_within_source=article.category_within_source,
                source_domain=article.source_domain,
                overall_sentiment_score=article.overall_sentiment_score,
                overall_sentiment_label=article.overall_sentiment_label,
            )

            session.add(db_article)
            session.flush()

            for topic in article.topics:
                db_topic = NewsTopic(
                    id=topic.id,
                    article_id=db_article.id,
                    topic=topic.topic,
                    relevance_score=topic.relevance_score
                )
                session.add(db_topic)

            for ticker in article.ticker_sentiment:
                db_ticker = NewsTickerSentiment(
                    id=ticker.id,
                    article_id=db_article.id,
                    ticker=ticker.ticker,
                    relevance_score=ticker.relevance_score,
                    ticker_sentiment_score=ticker.ticker_sentiment_score,
                    ticker_sentiment_label=ticker.ticker_sentiment_label
                )
                session.add(db_ticker)

            session.commit()
            print(f"Saved: {article.title}")
    except Exception as e:
        session.rollback()
        print(f"Error saving articles: {e}")
    finally:
        session.close()

def get_latest_news_titles_and_summaries(limit: int = 100) -> List[Dict[str, str]]:
    session: Session = SessionLocal()
    try:
        results = (
            session.query(NewsArticle.title, NewsArticle.summary)
            .order_by(NewsArticle.time_published.desc())
            .limit(limit)
            .all()
        )
        return [{"title": title, "summary": summary} for title, summary in results]
    finally:
        session.close()
        
if __name__ == "__main__":
    # articles = download_news_articles()
    # print(f"\nTotal articles fetched: {len(articles)}")
    # save_articles_to_db(articles)
    newsList=get_latest_news_titles_and_summaries()
    print(newsList)
