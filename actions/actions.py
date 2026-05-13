from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sys
import os

# Добавляем текущую папку в путь, чтобы RASA видел наши модули
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills_config import skills_weights, skill_to_skill, CRITICAL_SKILLS
from embeddings import extract_skills
from scoring import simple_scoring
from dijkstra_module import dijkstra_scoring

import networkx as nx

# ====================== GRAPH ======================
G = nx.Graph()
roles = ["project_manager", "data_analyst", "data_engineer", "data_scientist", "mlops_engineer"]

role_names_ru = {
    "project_manager": "Менеджер проекта",
    "data_analyst": "Дата-аналитик",
    "data_engineer": "Дата-инженер",
    "data_scientist": "Дата-сайентист",
    "mlops_engineer": "MLOps-инженер"
}

for role in roles:
    G.add_node(role)

for skill, weights in skills_weights.items():
    G.add_node(skill)
    for r, weight in weights.items():
        G.add_edge(skill, r, weight=weight)

for skill, targets in skill_to_skill.items():
    for target in targets:
        if target in skills_weights:
            G.add_edge(skill, target, weight=1)


class ValidateVacancyForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_vacancy_form"

    def validate_skills(self, slot_value, dispatcher, tracker, domain):
        if tracker.get_slot("requested_slot") != "skills":
            return {}
        
        raw_text = " ".join(slot_value) if isinstance(slot_value, list) else str(slot_value)
        skill_map = extract_skills(raw_text)
        skills_list = list(skill_map.keys())
        
        if not skills_list:
            dispatcher.utter_message(text="Не смог распознать навыки. Попробуй: python, sql, pandas")
            return {"skills": None}
        
        dispatcher.utter_message(text=f"✅ Распознанные навыки: {', '.join(skills_list)}")
        return {"skills": skills_list}


class ActionEvaluateCandidate(Action):
    def name(self) -> Text:
        return "action_evaluate_candidate"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        skills_text = " ".join(tracker.get_slot("skills") or [])
        skill_map = extract_skills(skills_text)

        scoring_scores = simple_scoring(skill_map, roles)
        dijkstra_scores = dijkstra_scoring(G, skill_map, roles)

        final_scores = {role: round((scoring_scores.get(role, 0) + dijkstra_scores.get(role, 0)) / 2) for role in roles}
        best_role = max(final_scores, key=final_scores.get)
        best_score = final_scores[best_role]

        text = f"🏆 Лучше всего ты подходишь на **{role_names_ru[best_role]}** — {best_score} баллов\n\n"
        
        for role in roles:
            text += f"• {role_names_ru[role]}: {final_scores[role]} баллов\n"

        critical = CRITICAL_SKILLS.get(best_role, [])
        missing_critical = [s for s in critical if s not in skill_map]
        if missing_critical:
            text += f"\n❌ Отсутствуют критические навыки: {missing_critical}"
        else:
            text += "\n✅ Подходишь по критическим навыкам!"

        missing = [s for s in skills_weights if s not in skill_map and G.has_edge(s, best_role)]
        if missing:
            text += f"\n\n🔧 Подкачать: {', '.join(missing[:10])}"

        dispatcher.utter_message(text=text)
        return []


# Для совместимости со старым кодом
class ActionShowCandidateData(Action):
    def name(self) -> Text:
        return "action_show_candidate_data"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Оценка кандидата завершена.")
        return []