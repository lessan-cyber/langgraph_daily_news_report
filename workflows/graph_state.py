from typing import List, Dict, TypedDict, Optional


class Article(TypedDict):
    """Represent an article  schema in the RSS feed."""

    title: str
    link: str
    published: str
    summary: Optional[str]
    category: Optional[str]
    content: Optional[str]


class GraphState(TypedDict):
    """
    Represents the state of the daily AI news workflow.
    This state is used to track the progress of the workflow,
    including articles fetched, filtered, classified, summarized,
    """

    all_articles: List[Article]
    filtered_articles: List[Article]
    categorized_articles: Dict[str, List[Article]]
    summaries: Dict[str, str]
    categories_to_process: List[str]
    current_category: Optional[str]
    # for debugging and logging
    workflow_messages: List[str]
