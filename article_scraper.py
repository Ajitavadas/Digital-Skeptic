import requests
from bs4 import BeautifulSoup
from newspaper import Article
import re
from typing import Dict, Optional
from config import Config


class ArticleScrapingError(Exception):
    """Custom exception for article scraping errors."""
    pass


class ArticleScraper:
    """Handles web scraping and content extraction from news article URLs."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': Config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

    def extract_article(self, url: str) -> Dict[str, str]:
        """
        Extract article content from URL using multiple fallback methods.

        Args:
            url (str): The URL of the news article

        Returns:
            Dict[str, str]: Dictionary containing article metadata and content

        Raises:
            ArticleScrapingError: If article extraction fails
        """
        try:
            # Method 1: Try newspaper3k (most reliable for news articles)
            article_data = self._extract_with_newspaper(url)
            if article_data['content'] and len(article_data['content'].strip()) > 100:
                return article_data

        except Exception as e:
            if Config.DEBUG_MODE:
                print(f"Newspaper3k extraction failed: {e}")

        try:
            # Method 2: Fallback to custom BeautifulSoup extraction
            article_data = self._extract_with_beautifulsoup(url)
            if article_data['content'] and len(article_data['content'].strip()) > 100:
                return article_data

        except Exception as e:
            if Config.DEBUG_MODE:
                print(f"BeautifulSoup extraction failed: {e}")

        raise ArticleScrapingError(f"Failed to extract meaningful content from URL: {url}")

    def _extract_with_newspaper(self, url: str) -> Dict[str, str]:
        """Extract article using newspaper3k library."""
        article = Article(url)
        article.download()
        article.parse()

        return {
            'title': article.title or 'Unknown Title',
            'content': article.text or '',
            'authors': ', '.join(article.authors) if article.authors else 'Unknown Author',
            'publish_date': str(article.publish_date) if article.publish_date else 'Unknown Date',
            'url': url,
            'extraction_method': 'newspaper3k'
        }

    def _extract_with_beautifulsoup(self, url: str) -> Dict[str, str]:
        """Extract article using BeautifulSoup with custom selectors."""
        response = self.session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = self._extract_title(soup)

        # Extract main content
        content = self._extract_content(soup)

        # Extract metadata
        authors = self._extract_authors(soup)

        return {
            'title': title,
            'content': content,
            'authors': authors,
            'publish_date': 'Unknown Date',
            'url': url,
            'extraction_method': 'beautifulsoup'
        }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title from HTML."""
        # Try multiple title selectors
        selectors = [
            'h1.entry-title',
            'h1.headline',
            'h1.article-title',
            '.headline h1',
            'article h1',
            'h1',
            'title'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                return element.get_text().strip()

        return 'Unknown Title'

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main article content from HTML."""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()

        # Try multiple content selectors
        selectors = [
            '.entry-content',
            '.article-content',
            '.post-content',
            '.story-body',
            'article .content',
            '[data-module="ArticleBody"]',
            '.article-body',
            'main article',
            'article'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                content = element.get_text(separator=' ', strip=True)
                if len(content) > 200:  # Ensure we have substantial content
                    return self._clean_content(content)

        # Fallback: extract all paragraph text
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text(strip=True) for p in paragraphs])
        return self._clean_content(content)

    def _extract_authors(self, soup: BeautifulSoup) -> str:
        """Extract author information from HTML."""
        # Try multiple author selectors
        selectors = [
            '.author',
            '.byline',
            '[rel="author"]',
            '.article-author',
            '.post-author'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                return element.get_text().strip()

        return 'Unknown Author'

    def _clean_content(self, content: str) -> str:
        """Clean and normalize article content."""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)

        # Remove common junk text
        junk_patterns = [
            r'Subscribe to.*?newsletter',
            r'Follow us on.*?social media',
            r'Copyright ©.*?rights reserved',
            r'This article was originally published.*?',
            r'Read more:.*?$'
        ]

        for pattern in junk_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.MULTILINE)

        # Truncate if too long
        if len(content) > Config.MAX_ARTICLE_LENGTH:
            content = content[:Config.MAX_ARTICLE_LENGTH] + "..."

        return content.strip()
