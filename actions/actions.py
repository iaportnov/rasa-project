from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


ROLE_REQUIREMENTS = {
    "Project Manager": {
        "agile": 2,
        "scrum": 2,
        "kanban": 1,
        "jira": 1,
        "confluence": 1,
        "управление проектами": 2,
        "проектное управление": 2,
        "управление командой": 2,
        "коммуникация": 2,
        "коммуникация с бизнесом": 2,
        "планирование": 1,
        "постановка задач": 1,
    },
    "Data Analyst": {
        "sql": 2,
        "python": 2,
        "pandas": 1,
        "numpy": 1,
        "power bi": 1,
        "tableau": 1,
        "excel": 1,
        "статистика": 2,
        "a/b testing": 2,
        "a/b тесты": 2,
        "аб тесты": 2,
        "метрики": 2,
        "дашборды": 1,
        "визуализация данных": 1,
        "анализ данных": 2,
    },
    "Data Engineer": {
        "sql": 2,
        "python": 2,
        "scala": 2,
        "java": 1,
        "etl": 2,
        "elt": 2,
        "airflow": 2,
        "spark": 2,
        "hadoop": 2,
        "kafka": 2,
        "dwh": 1,
        "data lake": 1,
        "хранилище данных": 1,
        "пайплайны данных": 2,
        "базы данных": 1,
    },
    "Data Scientist": {
        "python": 2,
        "pandas": 1,
        "numpy": 1,
        "sklearn": 2,
        "scikit-learn": 2,
        "catboost": 2,
        "xgboost": 2,
        "lightgbm": 2,
        "machine learning": 2,
        "ml": 2,
        "машинное обучение": 2,
        "глубокое обучение": 1,
        "deep learning": 1,
        "nlp": 1,
        "computer vision": 1,
        "компьютерное зрение": 1,
        "статистика": 1,
        "модели": 2,
    },
    "MLOps Engineer": {
        "python": 1,
        "docker": 2,
        "kubernetes": 2,
        "ci/cd": 2,
        "mlflow": 2,
        "dvc": 2,
        "linux": 1,
        "prometheus": 1,
        "grafana": 1,
        "мониторинг": 1,
        "monitoring": 1,
        "deployment": 2,
        "деплой": 2,
        "развертывание моделей": 2,
        "инфраструктура": 1,
    },
}


def normalize_skills(skills):
    if not skills:
        return []

    if isinstance(skills, str):
        skills = [skills]

    return [skill.lower().strip() for skill in skills]


def calculate_scores(skills, experience_years):
    scores = {role: 0 for role in ROLE_REQUIREMENTS}
    normalized_skills = normalize_skills(skills)

    for role, requirements in ROLE_REQUIREMENTS.items():
        for skill in normalized_skills:
            if skill in requirements:
                scores[role] += requirements[skill]

    try:
        experience_years = float(experience_years)
    except (TypeError, ValueError):
        experience_years = 0

    if experience_years >= 1:
        for role in scores:
            scores[role] += 1

    if experience_years >= 3:
        for role in scores:
            scores[role] += 1

    return scores


def analyze_salary(salary_expectation, experience_years):
    try:
        salary = float(salary_expectation)
    except (TypeError, ValueError):
        return "Зарплатные ожидания не были указаны достаточно понятно."

    try:
        experience = float(experience_years)
    except (TypeError, ValueError):
        experience = 0

    if salary <= 150000:
        return "Ваши зарплатные ожидания выглядят реалистично для junior-специалиста или начинающего middle-уровня."

    if 150000 < salary <= 250000:
        return "Ваши зарплатные ожидания выглядят реалистично для middle-специалиста."

    if 250000 < salary <= 350000:
        if experience >= 3:
            return "Ваши зарплатные ожидания достаточно высокие, но могут быть обоснованы при вашем уровне опыта."
        return "Ваши зарплатные ожидания выглядят довольно высокими для текущего уровня опыта."

    return "Ваши зарплатные ожидания очень высокие, поэтому рекрутеру может понадобиться дополнительное подтверждение вашего опыта и навыков."


def build_feedback(best_role, best_score, scores, salary_comment):
    if best_score >= 7:
        level = "высокий"
        decision = f"Вы хорошо подходите на роль {best_role}."
    elif best_score >= 4:
        level = "средний"
        decision = f"Вы частично подходите на роль {best_role}."
    else:
        level = "низкий"
        decision = "На данный момент вы не полностью подходите ни на одну из ролей в ML-команде."

    score_details = "\n".join(
        [f"- {role}: {score} баллов" for role, score in scores.items()]
    )

    if best_score >= 4:
        recommendation = (
            f"Больше всего вам подходит роль {best_role}. "
            "Чтобы усилить профиль, стоит развивать недостающие технические и практические навыки для этой роли."
        )
    else:
        recommendation = (
            "Рекомендуем начать с базовых навыков: SQL, Python, статистика, "
            "анализ данных или управление проектами — в зависимости от выбранного карьерного направления."
        )

    return (
        f"{decision}\n\n"
        f"Уровень соответствия: {level}\n\n"
        f"Баллы по ролям:\n{score_details}\n\n"
        f"Анализ зарплатных ожиданий: {salary_comment}\n\n"
        f"Рекомендация: {recommendation}"
    )


class ActionEvaluateCandidate(Action):

    def name(self) -> Text:
        return "action_evaluate_candidate"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        skills = tracker.get_slot("skills")
        experience_years = tracker.get_slot("experience_years")
        salary_expectation = tracker.get_slot("salary_expectation")

        scores = calculate_scores(skills, experience_years)

        best_role = max(scores, key=scores.get)
        best_score = scores[best_role]

        salary_comment = analyze_salary(salary_expectation, experience_years)

        feedback = build_feedback(best_role, best_score, scores, salary_comment)

        dispatcher.utter_message(text=feedback)

        return []
