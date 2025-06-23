from workflows.graph_state import GraphState, Article
from workflows.daily_ai_news import create_daily_ai_news_workflow

if __name__ == "__main__":
    import os
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    initial_state: GraphState = {
        "all_articles": [],
        "filtered_articles": [],
        "categorized_articles": {},
        "summaries": {},
        "categories_to_process": [],
        "current_category": None,
        "workflow_messages": [],
    }

    app = create_daily_ai_news_workflow()
    graph_png = app.get_graph().draw_mermaid_png()
    with open("workflow_graph.png", "wb") as f:
        f.write(graph_png)
    print("\n--- Workflow execution  ---")
    final_state = app.invoke(initial_state)

    print("\n--- workflow execution end : ---")
    print(f"total number of articles : {len(final_state['all_articles'])}")
    print(
        f"number of article after after applying the 'published yesterday' filter : {len(final_state['filtered_articles'])}"
    )

    if final_state.get("final_report_path"):
        print(f"\n--- final report generated : {final_state['final_report_path']} ---")
        print("\n open this file to see it .")
    else:
        print("\n--- No report has been generated. ---")
