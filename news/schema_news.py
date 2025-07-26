from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List, Optional

class NewsTopicSchema(BaseModel):
    topic: str
    relevance_score: float

class NewsTickerSentimentSchema(BaseModel):
    ticker: str
    relevance_score: float
    ticker_sentiment_score: float
    ticker_sentiment_label: str

class NewsArticleSchema(BaseModel):
    title: str
    url: HttpUrl
    time_published: datetime
    author: str
    summary: str
    banner_image: Optional[HttpUrl] = None
    source: str
    category_within_source: str
    source_domain: str
    overall_sentiment_score: float
    overall_sentiment_label: str
    topics: List[NewsTopicSchema]
    ticker_sentiment: List[NewsTickerSentimentSchema]

    class Config:
        from_attributes = True
