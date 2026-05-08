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
        "project management": 2,
        "team management": 2,
        "communication": 2,
        "planning": 1,
    },
    "Data Analyst": {
        "sql": 2,
        "python": 2,
        "pandas": 1,
        "numpy": 1,
        "power bi": 1,
        "tableau": 1,
        "excel": 1,
        "statistics": 2,
        "a/b testing": 2,
        "metrics": 2,
        "dashboards": 1,
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
    },
    "Data Scientist": {
        "python": 2,
        "pandas": 1,
        "numpy": 1,
        "sklearn": 2,
        "catboost": 2,
        "xgboost": 2,
        "lightgbm": 2,
        "machine learning": 2,
        "ml": 2,
        "deep learning": 1,
        "nlp": 1,
        "computer vision": 1,
        "statistics": 1,
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
        "monitoring": 1,
        "deployment": 2,
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
        return "Salary expectation was not clearly provided."

    try:
        experience = float(experience_years)
    except (TypeError, ValueError):
        experience = 0

    if salary <= 150000:
        return "Your salary expectations look realistic for a junior or early middle candidate."

    if 150000 < salary <= 250000:
        return "Your salary expectations look reasonable for a middle-level candidate."

    if 250000 < salary <= 350000:
        if experience >= 3:
            return "Your salary expectations are high, but they may be reasonable with your experience level."
        return "Your salary expectations are quite high for your current experience level."

    return "Your salary expectations are very high, so the recruiter may need additional justification based on your experience and skills."


def build_feedback(best_role, best_score, scores, salary_comment):
    if best_score >= 7:
        level = "high"
        decision = f"You are a good fit for the {best_role} role."
    elif best_score >= 4:
        level = "medium"
        decision = f"You partially fit the {best_role} role."
    else:
        level = "low"
        decision = "At the moment, you do not fully match any role in the ML project team."

    score_details = "\n".join(
        [f"- {role}: {score} points" for role, score in scores.items()]
    )

    if best_score >= 4:
        recommendation = (
            f"Your strongest match is {best_role}. "
            "To improve your profile, strengthen the missing technical and practical skills for this role."
        )
    else:
        recommendation = (
            "We recommend starting with basic skills such as SQL, Python, statistics, "
            "data analysis, or project management depending on your career interests."
        )

    return (
        f"{decision}\n\n"
        f"Match level: {level}\n\n"
        f"Scores:\n{score_details}\n\n"
        f"Salary expectation: {salary_comment}\n\n"
        f"Recommendation: {recommendation}"
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
