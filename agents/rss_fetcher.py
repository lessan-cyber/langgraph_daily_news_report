import feedparser
from typing import List
from workflows.graph_state import Article, GraphState
from config.settings import RSS_FEED


def rss_fetcher_agent(state: GraphState) -> GraphState:
    """ "This agent fetches articles from an RSS feed and adds them to the graph state by updating the 'all_aticles" variables."""
    print("-- RSS Fetcher Agent --")
    all
    all_articles: List[Article] = []
    workflow_message = state.get("workflow_message", [])

    for feed_url in RSS_FEED:
        try:
            print(f"Fetching articles from {feed_url}")
            feed = feedparser.parse(feed_url)
            if feed.bozo:
                error_message = f"Error parsing feed {feed_url}: {feed.bozo_exception}"
                print(error_message)
                workflow_message.append(error_message)
                continue
            for entry in feed.entries:
                title = entry.get("title", "No title")
                link = entry.get("link", "No link")
                summary = entry.get("summary", "No summary")
                published = entry.get("published", "No published date")

                article: Article = {
                    "title": title,
                    "link": link,
                    "published": published,
                    "summary": summary,
                    "category": None,  # it will be filled later
                    "content": None,  # it will be filled later
                }
                all_articles.append(article)
        except Exception as e:
            print(f"Error fetching articles from {feed_url}: {e}")
            continue
        state["all_articles"] = all_articles
    return state
