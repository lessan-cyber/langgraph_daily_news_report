from dotenv import load_dotenv
import os

load_dotenv()
# gettting the gemini api key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# rss feed configuration
RSS_FEED = [
    "https://www.theverge.com/rss/index.xml",
    "https://dev.to/feed",
    "https://techcrunch.com/feed/",
    "https://developer.nvidia.com/blog/feed",
    "http://ai.stanford.edu/blog/feed.xml",
    "https://news.ycombinator.com/rss",
    "http://feeds.feedburner.com/blogspot/gJZg",
    "https://www.microsoft.com/en-us/research/feed/",
    "https://bair.berkeley.edu/blog/feed.xml",
]


# classification categories
CATEGORIES = ["Artificial intelligence", "programming", "Startup", "Other"]
EXCLUDE_URL_KEYWORDS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".pdf",
    ".zip",
    ".mp4",
    ".avi",
    ".mov",
    "mailto:",
    "tel:",
    "#",
    "?",
]
EXCLUDE_HTML_SELECTORS = [
    "header",
    "footer",
    "nav",
    "aside",
    ".sidebar",
    ".ad",
    ".advertisement",
    ".meta",
    ".comment-section",
    "#comments",
    ".share-buttons",
    ".related-posts",
    ".author-box",
    "script",
    "style",
    "form",
    ".popup",
    ".popup-overlay",
    ".popup-content",
    ".popup-close",
    ".popup-background",
    ".popup-wrapper",
    ".popup-header",
    ".popup-footer",
    ".popup-body",
]
