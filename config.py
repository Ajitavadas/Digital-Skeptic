import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the Digital Skeptic AI."""

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')

    # Analysis Configuration
    MAX_ARTICLE_LENGTH = 10000  # Maximum characters to analyze
    MAX_RETRIES = 3  # Maximum retry attempts for failed requests

    # Debug Configuration
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

    # User Agent for web scraping
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required. Please set it in your .env file or environment variables."
            )
