from typing import List, Dict, Any
from datetime import datetime, timedelta, timezone
from workflows.graph_state import GraphState, Article
from dateutil.parser import parse as date_parse


def is_article_published_yesterday(article: Article) -> bool:
    """
    check if the article was published yesterday in UTC.
    Returns True if the article was published yesterday, False otherwise.
    If the date cannot be parsed, it logs a warning and returns False to ignore the article
    """
    # get today's date in UTC
    today_utc = datetime.now(timezone.utc).date()
    yesterday_utc = today_utc - timedelta(days=1)

    try:
        # Parse the 'published' date from the article
        article_datetime_utc = date_parse(article["published"]).astimezone(timezone.utc)
        article_date = article_datetime_utc.date()

        return article_date == yesterday_utc
    except Exception as e:
        # Log the error and return False to ignore the article
        print(
            f"Warning: Could not parse article date '{article['published']}' - {e}. Ignoring this article."
        )
        return False


# Le reste du fichier article_filter_agent reste inchangé
def article_filter_agent(state: GraphState) -> GraphState:
    """
    This agent filters articles that were published yesterday.
    It updates the state with the filtered articles and logs messages.
    """
    print("--- Filter agent  ---")
    all_articles = state["all_articles"]
    filtered_articles: List[Article] = []
    workflow_messages = state.get("workflow_messages", [])

    if not all_articles:
        message = " no articles found in the state to filter."
        print(message)
        workflow_messages.append(message)
        return {
            **state,
            "filtered_articles": [],
            "workflow_messages": workflow_messages,
        }

    for article in all_articles:
        if is_article_published_yesterday(article):
            filtered_articles.append(article)

    print(
        f"--- ArticleFilter completed, number of article published yesterday : {len(filtered_articles)} / {len(all_articles)} ---"
    )
    if not filtered_articles:
        workflow_messages.append("no article found after.")

    state["filtered_articles"] = filtered_articles
    state["workflow_messages"] = workflow_messages
    return state
