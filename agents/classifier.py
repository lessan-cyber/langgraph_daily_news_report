from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from workflows.graph_state import GraphState, Article
from config.settings import GOOGLE_API_KEY, CATEGORIES
from config.prompts import CLASSIFICATION_PROMPT


def classify_agent(state: GraphState) -> GraphState:
    """
    This agent classifies articles into categories using a language model.
    It updates the state with the classified articles and logs messages.
    """
    print("---- Classifier Agent ----")
    filtered_articles: List[Article] = state["filtered_articles"]
    workflow_messages = state.get("workflow_messages", [])

    # Initialize the language model
    llm = ChatGoogleGenerativeAI(
        google_api_key=GOOGLE_API_KEY, model="gemini-2.0-flash", temperature=0
    )

    prompt = ChatPromptTemplate.from_template(CLASSIFICATION_PROMPT)

    categorized_articles: Dict[str, List[Article]] = {
        category: [] for category in CATEGORIES
    }

    if not filtered_articles:
        message = "No articles found to classify."
        print(message)
        workflow_messages.append(message)
        return {
            **state,
            "categorized_articles": categorized_articles,
            "workflow_messages": workflow_messages,
        }

    for i, article in enumerate(filtered_articles):
        print(
            f"Classifying article {i + 1}/{len(filtered_articles)}: {article['title']}"
        )
        try:
            # prepare the input for the llm
            input_data = {
                "categories": ", ".join(CATEGORIES),
                "article_title": article["title"],
                "article_summary": article["summary"]
                if article["summary"]
                else article["title"],
            }
            # Chain the prompt with the input data
            chain = prompt | llm
            response = chain.invoke(input_data)
            predicted_category = response.content.strip()
            if predicted_category in CATEGORIES:
                article["category"] = predicted_category
                categorized_articles[predicted_category].append(article)
                print(
                    f"Article classified as '{predicted_category}': {article['title']}"
                )
            else:
                article["category"] = "Other"
                categorized_articles["Other"].append(article)
                workflow_messages.append(
                    f"LLM returned an unexpected category: {predicted_category}. Article classified as 'Other'."
                )
        except Exception as e:
            error_message = f"    Erreur lors de la classification de '{article['title']}': {e}. Classé comme 'Autre'."
            print(error_message)
            workflow_messages.append(error_message)
            article["category"] = "Other"
            categorized_articles[""].append(article)
    print(
        f"--- Classification completed, number of articles classified: {len(filtered_articles)} ---"
    )
    categories_with_articles = [
        cat for cat, articles in categorized_articles.items() if articles
    ]
    state["categorized_articles"] = categorized_articles
    state["categories_to_process"] = categories_with_articles
    state["workflow_messages"] = workflow_messages
    return state
