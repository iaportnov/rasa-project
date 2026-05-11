from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import networkx as nx
from sentence_transformers import SentenceTransformer, util
import torch
import re

# ====================== 1. GRAPH (Skill Knowledge Graph) ======================
G = nx.Graph()

roles = ["project_manager", "data_analyst", "data_engineer", "data_scientist", "mlops_engineer"]

role_names_ru = {
    "project_manager": "Project Manager",
    "data_analyst": "Data Analyst",
    "data_engineer": "Data Engineer",
    "data_scientist": "Data Scientist",
    "mlops_engineer": "MLOps Engineer"
}

# Добавляем роли
for role in roles:
    G.add_node(role)

# Веса навыков (можно менять)
skills_weights = {
    "python":           {"data_scientist": 2, "data_analyst": 1, "data_engineer": 1, "mlops_engineer": 2, "project_manager": 4},
    "sql":              {"data_scientist": 2, "data_analyst": 1, "data_engineer": 1, "mlops_engineer": 3, "project_manager": 4},
    "pandas":           {"data_scientist": 2, "data_analyst": 1, "data_engineer": 3, "mlops_engineer": 4, "project_manager": 5},
    "pytorch":          {"data_scientist": 1, "data_analyst": 4, "data_engineer": 4, "mlops_engineer": 3, "project_manager": 5},
    "tensorflow":       {"data_scientist": 1, "data_analyst": 4, "data_engineer": 4, "mlops_engineer": 3, "project_manager": 5},
    "scikit-learn":     {"data_scientist": 2, "data_analyst": 2, "data_engineer": 4, "mlops_engineer": 4, "project_manager": 5},
    "docker":           {"mlops_engineer": 1, "data_engineer": 2, "data_scientist": 3, "data_analyst": 5, "project_manager": 5},
    "kubernetes":       {"mlops_engineer": 1, "data_engineer": 2, "data_scientist": 4, "data_analyst": 5, "project_manager": 5},
    "airflow":          {"data_engineer": 1, "mlops_engineer": 2, "data_scientist": 3, "data_analyst": 4, "project_manager": 5},
    "kafka":            {"data_engineer": 1, "mlops_engineer": 2, "data_scientist": 4, "data_analyst": 5, "project_manager": 5},
    "project_management":{"project_manager": 1, "data_analyst": 3, "data_scientist": 4, "data_engineer": 4, "mlops_engineer": 4},
}

for skill, weights in skills_weights.items():
    G.add_node(skill)
    for role, weight in weights.items():
        G.add_edge(skill, role, weight=weight)

# ====================== 2. EMBEDDINGS ======================
embedder = SentenceTransformer('all-MiniLM-L6-v2')
known_skills = list(skills_weights.keys())

def extract_skills(user_text: str, threshold: float = 0.45) -> List[str]:
    if not user_text or not user_text.strip():
        return []
    
    chunks = re.split(r'[,\s]+и\s+|[,\s]+с\s+|[,\s]+', user_text.lower())
    chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 2]
    
    extracted = []
    for chunk in chunks:
        user_emb = embedder.encode(chunk, convert_to_tensor=True)
        known_embs = embedder.encode(known_skills, convert_to_tensor=True)
        cos_scores = util.cos_sim(user_emb, known_embs)[0]
        top_idx = torch.argmax(cos_scores).item()
        score = cos_scores[top_idx].item()
        
        if score >= threshold:
            extracted.append(known_skills[top_idx])
    return extracted

# ====================== 3. CUSTOM ACTION ======================
class ActionEvaluateCandidate(Action):

    def name(self) -> Text:
        return "action_evaluate_candidate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Получаем данные из слотов формы
        position = tracker.get_slot("position")
        years = tracker.get_slot("years_experience") or 0.0
        skills_text = " ".join(tracker.get_slot("key_skills") or [])
        salary = tracker.get_slot("expected_salary") or 0

        # Извлекаем навыки через embeddings
        candidate_skills = extract_skills(skills_text)

        # Оценка по ролям
        scores = {}
        for role in roles:
            total_weight = 0
            used = 0
            for skill in candidate_skills:
                if G.has_edge(skill, role):
                    total_weight += G[skill][role]['weight']
                    used += 1
            
            distance = total_weight / used if used > 0 else 999
            score = max(0, 100 - int(distance * 12))
            
            # Бонус, если позиция совпадает с выбранной
            if role == position:
                score = min(100, score + 25)
            
            scores[role] = score

        best_role = max(scores, key=scores.get)
        best_score = scores[best_role]

        # Формируем красивый ответ
        message = f"Я проанализировал твои данные.\n\n"
        message += f"📊 Лучше всего ты подходишь на **{role_names_ru[best_role]}** — {best_score} баллов\n\n"
        message += "Оценка по всем позициям:\n"
        
        for role, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            message += f"• {role_names_ru[role]}: {score} баллов\n"

        if best_score >= 75:
            message += "\n✅ Отлично! Ты сильный кандидат, рекомендую идти дальше."
        elif best_score >= 55:
            message += "\n⚠️ Хороший результат. Есть потенциал для роста."
        else:
            message += "\n❌ Пока не совсем подходит под наши требования, но спасибо за интервью!"

        dispatcher.utter_message(text=message)

        # Завершаем форму
        return [SlotSet("screening_complete", True)]