import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from workflows.graph_state import GraphState, Article
from requests.exceptions import RequestException
from config.settings import EXCLUDE_HTML_SELECTORS, EXCLUDE_URL_KEYWORDS, CATEGORIES
import time


def clean_html_content(html_content: str) -> str:
    """ "Clean HTML content by removing unwanted tags and attributes."""
    if not html_content:
        return ""

    soup = BeautifulSoup(html_content, "html.parser")

    # Remove unwanted HTML selectors
    for selector in EXCLUDE_HTML_SELECTORS:
        for element in soup.select(selector):
            element.decompose()

    main_content_tag = None
    possible_main_tags = ["article", "main", "div", "section"]
    for tag_name in possible_main_tags:
        # Essayer de trouver la balise avec une classe ou un ID commun pour le contenu principal
        main_content_tag = soup.find(
            tag_name,
            class_=[
                "entry-content",
                "post-content",
                "article-content",
                "main-content",
                "single-content",
            ],
        )
        if main_content_tag:
            break

    if not main_content_tag:
        main_content_tag = soup.find("body")

    # Extract text and clean it
    text = ""
    if main_content_tag:
        text = main_content_tag.get_text(separator="\n", strip=True)
    else:
        text = soup.get_text(separator="\n", strip=True)

    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

    MAX_CONTENT_LENGTH = 15000
    if len(text) > MAX_CONTENT_LENGTH:
        text = (
            text[:MAX_CONTENT_LENGTH]
            + "...\n[CONTENU TRONQUÉ POUR LA LIMITE DE TAILLE]"
        )
    return text


def fetch_article_content(url: str, retries: int = 3, delay: int = 2) -> str:
    """ " Fetch article content from a URL with retries"""
    if any(keyword in url for keyword in EXCLUDE_URL_KEYWORDS):
        return None
    for i in range(retries):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"    retrie {i + 1}/{retries} for {url}: {e}")
            if i < retries - 1:
                time.sleep(delay)
            else:
                return None
        except Exception as e:
            print(f"  unexpected error for {url}: {e}")
            return None
    return None


def content_extractor_agent(state: GraphState) -> GraphState:
    """ "
    Agent reponsible for extracting content from articles in the graph state.
    """
    print("--- Content Extractor Agent ---")
    categories_articles = state["categorized_articles"]
    workflow_messages = state.get("workflow_messages", [])

    # check if there are classified articles to process
    if not categories_articles or all(
        not articles for articles in categories_articles.values()
    ):
        message = "No articles to process."
        print(message)
        workflow_messages.append(message)
        state["workflow_messages"] = workflow_messages
        return state

    for category, articles in categories_articles.items():
        print(f"Processing category: {category} ({len(articles)} articles)")

        for i, article in enumerate(articles):
            print(
                f"    Traitement de l'article {i + 1}/{len(articles)}: '{article['title']}'"
            )
            article_url = article["link"]
            # handle invalid URLs and empty titles
            if not article_url or not article_url.startswith(("http://", "https://")):
                message = f"      invalid link {article['title']}'."
                print(message)
                workflow_messages.append(message)
                article["content"] = "[CONTENT NOT AVAILABLE DUE TO INVALID URL]"
                continue
            html_content = fetch_article_content(article_url)

            if html_content:
                cleaned_text = clean_html_content(html_content)
                article["content"] = cleaned_text
                if not cleaned_text:
                    message = f"Empty content for article '{article['title']}'"
                    print(message)
                    workflow_messages.append(message)
            else:
                message = f"Failed to fetch content for article '{article['title']}'"
                print(message)
                workflow_messages.append(message)
                article["content"] = "[CONTENT NOT AVAILABLE DUE TO FETCH ERROR]"
    print("--- Content extraction completed ---")
    state["workflow_messages"] = workflow_messages
    state["categorized_articles"] = categories_articles
    return state
