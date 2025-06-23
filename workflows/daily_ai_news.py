from typing_extensions import Literal
from langgraph.graph import StateGraph, END
from typing import List, Dict, Any, Dict, Optional
from agents.rss_fetcher import rss_fetcher_agent
from workflows.graph_state import GraphState, Article
from agents.article_filter import article_filter_agent
from agents.classifier import classify_agent
from agents.content_extractor import content_extractor_agent
from agents.orchestrator import (
    decide_next_step,
    update_orchestration_state,
)
from agents.summarizer import summarize_agent
from agents.report_generator import report_generator_agent


# La fonction de décision post-classification reste inchangée
def decide_on_classification_outcome(
    state: GraphState,
) -> Literal["start_orchestration", "no_articles_to_process"]:
    """
    Decide wether to start orchestration or end the workflow based on classified articles.
    """
    categorized_articles = state.get("categorized_articles", {})

    if any(articles for articles in categorized_articles.values()):
        print("articles found start orchestration")
        return "start_orchestration"
    else:
        print("  no articles found, end workflow")
        return "no_articles_to_process"


def create_daily_ai_news_workflow():
    """
    this function creates the daily AI news workflow using LangGraph.
    It sets up the state graph with nodes representing different agents,
    defines the edges for transitions between these nodes,
    and compiles the workflow into an application.
    The workflow includes fetching RSS feeds, filtering articles,
    classifying articles, extracting content, summarizing by category,
    and updating the orchestration state for iterative processing.
    The workflow is designed to handle articles in a loop,
    processing each category iteratively until all articles are processed.
    """
    workflow = StateGraph(GraphState)

    # 1. adding nodes (agents)
    workflow.add_node("fetch_rss", rss_fetcher_agent)
    workflow.add_node("filter_articles", article_filter_agent)
    workflow.add_node("classify_articles", classify_agent)
    workflow.add_node("extract_content", content_extractor_agent)
    workflow.add_node("summarize_category", summarize_agent)
    workflow.add_node("update_orchestration_state", update_orchestration_state)
    workflow.add_node("generate_report", report_generator_agent)
    # 2. defining edges
    workflow.set_entry_point("fetch_rss")
    workflow.add_edge("fetch_rss", "filter_articles")
    workflow.add_edge("filter_articles", "classify_articles")

    workflow.add_conditional_edges(
        "classify_articles",
        decide_on_classification_outcome,
        {
            "start_orchestration": "update_orchestration_state",
            "no_articles_to_process": END,
        },
    )

    workflow.add_conditional_edges(
        "update_orchestration_state",
        decide_next_step,
        {"process_category": "extract_content", "end_workflow": "generate_report"},
    )

    workflow.add_edge("extract_content", "summarize_category")

    workflow.add_edge("summarize_category", "update_orchestration_state")
    workflow.add_edge("generate_report", END)

    # 3. compiling the workflow
    app = workflow.compile()
    print("--- Graphe LangGraph compilé avec succès ! ---")
    return app
