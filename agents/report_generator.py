from typing import Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from workflows.graph_state import GraphState, Article
from config.settings import GOOGLE_API_KEY
from config.prompts import FINAL_REPORT_PROMPT
from datetime import datetime
import os


def report_generator_agent(state: GraphState) -> GraphState:
    """
    Agent reponsible for generating a final report based on the summaries of categorized articles."""
    print("----Generating final report...----")
    summaries: Dict[str, str] = state.get("summaries", {})
    workflow_messages = state.get("workflow_messages", [])

    if not summaries:
        message = "No summaries available to generate a report."
        workflow_messages.append(message)
        print(message)
        state["workflow_messages"] = workflow_messages
        return state

    # prepare the content of the summaries for the prompt
    summaries_formatted_for_llm = []

    for category, summary_text in summaries.items():
        summaries_formatted_for_llm.append(
            f"Category: {category}\nSummary: {summary_text}"
        )
    full_summaries_content = "\n\n".join(summaries_formatted_for_llm)
    llm = ChatGoogleGenerativeAI(
        google_api_key=GOOGLE_API_KEY, model="gemini-2.0-flash", temperature=0.1
    )

    # creating the prompt template
    prompt = ChatPromptTemplate.from_template(FINAL_REPORT_PROMPT)

    # generating the report

    generated_report = ""

    try:
        input_data = {
            "summaries_content": full_summaries_content,
            "report_date": datetime.now().strftime("%Y-%m-%d"),
        }
        chain = prompt | llm
        response = chain.invoke(input_data)
        generated_report = response.content.strip()
        report_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path = f"reports/{report_filename}"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as report_file:
            report_file.write(generated_report)
        message = f"Report generated successfully: {report_filename}"
        print(message)
        workflow_messages.append(message)
        state["workflow_messages"] = workflow_messages
        state["generated_report"] = generated_report
    except Exception as e:
        message = f"Error generating report: {str(e)}"
        print(message)
        workflow_messages.append(message)
        state["workflow_messages"] = workflow_messages
        state["generated_report"] = "REPORT NOT AVAILABLE DUE TO AN ERROR"
    return state
