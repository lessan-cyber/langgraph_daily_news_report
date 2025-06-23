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

    print("\n--- Exécution du workflow LangGraph ---")
    final_state = app.invoke(initial_state)

    print("\n--- Workflow Terminé. État final du graphe : ---")
    print(
        f"Nombre total d'articles bruts récupérés : {len(final_state['all_articles'])}"
    )
    print(
        f"Nombre d'articles filtrés (publiés hier) : {len(final_state['filtered_articles'])}"
    )

    print("\n--- Résumés générés par catégorie : ---")
    if final_state["summaries"]:
        for category, summary in final_state["summaries"].items():
            print(f"\n### Catégorie: {category.upper()} ###")
            print(summary)
            print("-" * 50)
    else:
        print("Aucun résumé généré.")

    if final_state["workflow_messages"]:
        print("\n--- Messages du Workflow : ---")
        for msg in final_state["workflow_messages"]:
            print(f"- {msg}")

    if final_state.get("final_report_path"):
        print(f"\n--- Rapport final généré : {final_state['final_report_path']} ---")
        print("\nOuvrez ce fichier pour consulter le rapport complet.")
    else:
        print("\n--- Aucun rapport final n'a été généré. ---")
