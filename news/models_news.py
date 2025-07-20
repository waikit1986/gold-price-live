import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy.dialects.postgresql import UUID


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    time_published = Column(DateTime, nullable=False)
    author = Column(String)
    summary = Column(Text)
    banner_image = Column(String)
    source = Column(String)
    category_within_source = Column(String)
    source_domain = Column(String)
    overall_sentiment_score = Column(Float)
    overall_sentiment_label = Column(String)

    # Relationships
    topics = relationship("NewsTopic", back_populates="article", cascade="all, delete-orphan")
    ticker_sentiments = relationship("NewsTickerSentiment", back_populates="article", cascade="all, delete-orphan")


class NewsTopic(Base):
    __tablename__ = "news_topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("news_articles.id"), nullable=False)
    topic = Column(String, nullable=False)
    relevance_score = Column(Float)

    article = relationship("NewsArticle", back_populates="topics")


class NewsTickerSentiment(Base):
    __tablename__ = "news_ticker_sentiments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("news_articles.id"), nullable=False)
    ticker = Column(String, nullable=False)
    relevance_score = Column(Float)
    ticker_sentiment_score = Column(Float)
    ticker_sentiment_label = Column(String)

    article = relationship("NewsArticle", back_populates="ticker_sentiments")
