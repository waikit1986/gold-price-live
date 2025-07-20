import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from news.functions_news import download_news_articles

if __name__ == "__main__":
    download_news_articles()
