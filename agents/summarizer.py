from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from workflows.graph_state import GraphState, Article
from config.prompts import SUMMARY_PROMPT
from config.settings import GOOGLE_API_KEY


def summarize_agent(state: GraphState) -> GraphState:
    """
    Agent responsible for summarizing articles in graph state.
    it updates the 'summaries" in the graph state
    """
    print("---Summarzing Agent---")
    current_category = state.get("current_category")
    categorized_articles = state["categorized_articles"]
    workflow_messages = state["workflow_messages"]
    llm = ChatGoogleGenerativeAI(
        google_api_key=GOOGLE_API_KEY, model="gemini-2.0-flash", temperature=0.5
    )
    if not current_category:
        message = "No current category set. Cannot summarize articles."
        print(message)
        workflow_messages.append(message)
        state["workflow_messages"] = workflow_messages
        return state

    articles_to_summarize: List[Article] = categorized_articles.get(
        current_category, []
    )

    if not articles_to_summarize:
        message = f"No articles to summarize in category '{current_category}'."
        print(message)
        workflow_messages.append(message)
        state["workflow_messages"] = workflow_messages
        return state

    relevant_contents = [
        f"Titre: {art['title']}\nLien: {art['link']}\nContenu:\n{art['content']}"
        for art in articles_to_summarize
        if art["content"] and "[CONTENU NON DISPONIBLE]" not in art["content"]
    ]
    if not relevant_contents:
        message = "No relevant content found in articles to summarize."
        print(message)
        workflow_messages.append(message)
        state["workflow_messages"] = workflow_messages
        updated_summaries = state.get("summaries", {})
        updated_summaries[current_category] = "No relevant content found."
        return state

    article_concatenated = "\n\n--- ARTICLE SUIVANT ---\n\n".join(relevant_contents)

    # initialize the Google Generative AI client
    prompt = ChatPromptTemplate.from_template(SUMMARY_PROMPT)

    print(
        "Generating summary for category:",
        current_category,
        "with",
        len(relevant_contents),
        "articles",
    )

    try:
        input_data = {
            "category_name": current_category,
            "articles_content": article_concatenated,
        }
        # chain the input data with the prompt
        chain = prompt | llm
        response = chain.invoke(input_data)
        # update the summaries in the state
        updated_summaries = state.get("summaries", {})
        updated_summaries[current_category] = response.content.strip()
        print(f"Summary for category '{current_category}' generated successfully.")
        workflow_messages.append(
            f"Summary for category '{current_category}' generated successfully."
        )
        state["summaries"] = updated_summaries
        state["workflow_messages"] = workflow_messages
        return state
    except Exception as e:
        error_message = (
            f"Error generating summary for category '{current_category}': {e}"
        )
        print(error_message)
        workflow_messages.append(error_message)
        state["workflow_messages"] = workflow_messages
        updated_summaries = state.get("summaries", {})
        updated_summaries[current_category] = "Error generating summary: " + str(e)
        state["summaries"] = updated_summaries
        return state
