from typing import List, Dict, Literal
from workflows.graph_state import GraphState, Article


def update_orchestration_state(state: GraphState) -> Dict:
    """
    Fonction de nœud qui met à jour l'état d'orchestration (sélectionne la prochaine catégorie,
    supprime la catégorie traitée). Retourne un dictionnaire d'updates.
    """
    print("--- Démarrage de la logique de mise à jour de l'Orchestrateur ---")
    workflow_messages = state.get("workflow_messages", [])

    categories_to_process = state.get(
        "categories_to_process", []
    ).copy()  # Faire une copie pour modification
    current_category = state.get("current_category")

    # Si nous venons de terminer une catégorie, la retirer de la liste
    if current_category and current_category in categories_to_process:
        print(f"  Catégorie '{current_category}' terminée. Suppression de la liste.")
        categories_to_process.remove(current_category)

    next_category = None
    if categories_to_process:
        next_category = categories_to_process[0]
        print(f"  Prochaine catégorie à préparer : '{next_category}'")
    else:
        print("  Toutes les catégories ont été traitées ou aucune catégorie à traiter.")

    return {
        "categories_to_process": categories_to_process,
        "current_category": next_category,
        "workflow_messages": workflow_messages,  # Assurez-vous que les messages sont passés
    }


def decide_next_step(state: GraphState) -> Literal["process_category", "end_workflow"]:
    """
    Fonction de routage qui décide de la prochaine étape du workflow basée sur l'état.
    Retourne une chaîne de caractères.
    """
    print("--- Orchestrator: Décision de la prochaine étape ---")
    current_category = state.get("current_category")

    if current_category:
        print(f"  Décision: Traiter la catégorie '{current_category}'.")
        return "process_category"
    else:
        print("  Décision: Aucune catégorie à traiter. Fin du workflow.")
        return "end_workflow"
