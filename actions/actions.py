from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# Структура навыков по ролям:
# - critical: критические навыки, без которых роль не подходит (суммарно 30-35 баллов)
# - main: основные навыки, must have (суммарно 50 баллов)
# - additional: дополнительные навыки, nice to have (суммарно 15-20 баллов)
# Суммарный максимум по роли = 100 баллов
ROLE_SKILLS = {
    "Менеджер проекта": {
        "critical": {
            "project_management": 12,
            "stakeholder_management": 10,
            "agile_scrum": 8,
        },
        "main": {
            "jira": 7,
            "risk_management": 7,
            "roadmap_planning": 7,
            "team_leadership": 7,
            "business_analysis": 6,
            "confluence": 5,
            "budgeting": 5,
            "ml_project_lifecycle": 6,
        },
        "additional": {
            "kanban": 3,
            "miro": 3,
            "sql": 4,
            "product_metrics": 4,
            "presentation_skills": 3,
            "english": 3,
        },
    },

    "Дата-аналитик": {
        "critical": {
            "sql": 15,
            "python": 10,
            "pandas": 10,
        },
        "main": {
            "statistics": 8,
            "data_visualization": 7,
            "tableau": 5,
            "power_bi": 5,
            "numpy": 4,
            "ab_testing": 7,
            "excel": 4,
            "matplotlib": 4,
            "seaborn": 3,
            "product_metrics": 3,
        },
        "additional": {
            "airflow": 3,
            "clickhouse": 3,
            "superset": 2,
            "dbt": 3,
            "jupyter": 2,
            "git": 2,
        },
    },

    "Дата-инженер": {
        "critical": {
            "sql": 12,
            "python": 12,
            "etl": 11,
        },
        "main": {
            "airflow": 8,
            "spark": 8,
            "kafka": 7,
            "postgresql": 5,
            "clickhouse": 5,
            "hadoop": 4,
            "docker": 5,
            "data_warehousing": 4,
            "dbt": 4,
        },
        "additional": {
            "linux": 3,
            "bash": 2,
            "greenplum": 2,
            "nosql": 3,
            "git": 2,
            "cicd": 3,
        },
    },

    "Дата-сайентист": {
        "critical": {
            "python": 12,
            "machine_learning": 13,
            "statistics": 10,
        },
        "main": {
            "pandas": 5,
            "numpy": 4,
            "scikit_learn": 7,
            "pytorch": 6,
            "tensorflow": 5,
            "sql": 5,
            "deep_learning": 6,
            "nlp": 4,
            "computer_vision": 4,
            "xgboost": 4,
        },
        "additional": {
            "mlflow": 3,
            "jupyter": 2,
            "git": 2,
            "matplotlib": 2,
            "catboost": 3,
            "hugging_face": 3,
        },
    },

    "MLOps-инженер": {
        "critical": {
            "python": 10,
            "docker": 13,
            "kubernetes": 12,
        },
        "main": {
            "cicd": 8,
            "mlflow": 7,
            "airflow": 5,
            "linux": 5,
            "bash": 4,
            "aws": 5,
            "terraform": 4,
            "monitoring": 6,
            "git": 3,
            "model_serving": 3,
        },
        "additional": {
            "gitlab_ci": 3,
            "prometheus": 3,
            "grafana": 2,
            "kubeflow": 3,
            "jenkins": 2,
            "ansible": 2,
        },
    },
}


# Синонимы навыков: разговорные варианты -> канонические названия
SKILL_SYNONYMS = {
    # Языки и базовые
    "питон": "python",
    "пайтон": "python",
    "py": "python",
    "скл": "sql",
    "эскюэль": "sql",
    "пандас": "pandas",
    "панды": "pandas",
    "нампай": "numpy",
    "намп": "numpy",
    "эксель": "excel",
    "скала": "scala",
    "ява": "java",

    # ML фреймворки
    "торч": "pytorch",
    "пайторч": "pytorch",
    "тензорфлоу": "tensorflow",
    "тф": "tensorflow",
    "склерн": "scikit_learn",
    "sklearn": "scikit_learn",
    "scikit-learn": "scikit_learn",
    "кэтбуст": "catboost",
    "хгбуст": "xgboost",
    "лайтгбм": "lightgbm",
    "хаггинг": "hugging_face",
    "huggingface": "hugging_face",
    "hugging face": "hugging_face",

    # ML понятия
    "ml": "machine_learning",
    "мл": "machine_learning",
    "машинное обучение": "machine_learning",
    "дл": "deep_learning",
    "глубокое обучение": "deep_learning",
    "нлп": "nlp",
    "обработка естественного языка": "nlp",
    "cv": "computer_vision",
    "компьютерное зрение": "computer_vision",
    "статистика": "statistics",
    "матстат": "statistics",
    "ab-тесты": "ab_testing",
    "ab тесты": "ab_testing",
    "аб тесты": "ab_testing",
    "a/b testing": "ab_testing",

    # BI и визуализация
    "повер би": "power_bi",
    "powerbi": "power_bi",
    "power bi": "power_bi",
    "табло": "tableau",
    "matplotlib": "matplotlib",
    "матплотлиб": "matplotlib",
    "сиборн": "seaborn",
    "визуализация": "data_visualization",
    "визуализация данных": "data_visualization",
    "дашборды": "data_visualization",
    "продуктовые метрики": "product_metrics",
    "метрики": "product_metrics",

    # Data Engineering
    "эирфлоу": "airflow",
    "аирфлоу": "airflow",
    "спарк": "spark",
    "кафка": "kafka",
    "хадуп": "hadoop",
    "постгрес": "postgresql",
    "постгря": "postgresql",
    "клик": "clickhouse",
    "кликхаус": "clickhouse",
    "хранилище данных": "data_warehousing",
    "dwh": "data_warehousing",
    "пайплайны": "etl",
    "пайплайны данных": "etl",
    "elt": "etl",

    # MLOps / DevOps
    "докер": "docker",
    "кубер": "kubernetes",
    "k8s": "kubernetes",
    "кубернетес": "kubernetes",
    "ci/cd": "cicd",
    "ci-cd": "cicd",
    "сицд": "cicd",
    "млфлоу": "mlflow",
    "линукс": "linux",
    "баш": "bash",
    "терраформ": "terraform",
    "мониторинг": "monitoring",
    "прометей": "prometheus",
    "прометеус": "prometheus",
    "графана": "grafana",
    "дженкинс": "jenkins",
    "гитлаб": "gitlab_ci",
    "гит": "git",
    "ансибл": "ansible",
    "деплой": "model_serving",
    "развертывание моделей": "model_serving",

    # PM
    "agile": "agile_scrum",
    "scrum": "agile_scrum",
    "аджайл": "agile_scrum",
    "скрам": "agile_scrum",
    "канбан": "kanban",
    "джира": "jira",
    "конфлюенс": "confluence",
    "управление проектами": "project_management",
    "проектное управление": "project_management",
    "управление командой": "team_leadership",
    "лидерство": "team_leadership",
    "работа с заказчиком": "stakeholder_management",
    "коммуникация с бизнесом": "stakeholder_management",
    "управление стейкхолдерами": "stakeholder_management",
    "управление рисками": "risk_management",
    "роадмап": "roadmap_planning",
    "планирование": "roadmap_planning",
    "бюджетирование": "budgeting",
    "бизнес-анализ": "business_analysis",
    "ml-проекты": "ml_project_lifecycle",
    "английский": "english",
    "презентация": "presentation_skills",
}


# Зарплатные вилки по ролям (в тыс. руб.) для разных уровней опыта
# Формат: (junior_max, middle_max, senior_max)
SALARY_RANGES = {
    "Менеджер проекта": (180, 280, 400),
    "Дата-аналитик": (150, 250, 350),
    "Дата-инженер": (180, 300, 450),
    "Дата-сайентист": (180, 320, 500),
    "MLOps-инженер": (200, 320, 450),
}


ROLE_SYNONYMS = {
    # Дата-аналитик
    "дата-аналитик": "Дата-аналитик",
    "дата аналитик": "Дата-аналитик",
    "аналитик": "Дата-аналитик",
    "аналитик данных": "Дата-аналитик",
    "продуктовый аналитик": "Дата-аналитик",
    "bi-аналитик": "Дата-аналитик",
    "би-аналитик": "Дата-аналитик",
    "data analyst": "Дата-аналитик",

    # Дата-сайентист
    "дата-сайентист": "Дата-сайентист",
    "дата сайентист": "Дата-сайентист",
    "сайентист": "Дата-сайентист",
    "data scientist": "Дата-сайентист",
    "специалист по машинному обучению": "Дата-сайентист",
    "ml-специалист": "Дата-сайентист",
    "ml специалист": "Дата-сайентист",
    "machine learning engineer": "Дата-сайентист",

    # Дата-инженер
    "дата-инженер": "Дата-инженер",
    "дата инженер": "Дата-инженер",
    "инженер данных": "Дата-инженер",
    "data engineer": "Дата-инженер",

    # Менеджер проекта
    "менеджер проекта": "Менеджер проекта",
    "проектный менеджер": "Менеджер проекта",
    "проджект": "Менеджер проекта",
    "проджект менеджер": "Менеджер проекта",
    "project manager": "Менеджер проекта",
    "pm": "Менеджер проекта",

    # MLOps-инженер
    "mlops-инженер": "MLOps-инженер",
    "mlops инженер": "MLOps-инженер",
    "mlops engineer": "MLOps-инженер",
    "mlops": "MLOps-инженер",
    "инженер mlops": "MLOps-инженер",
}


def normalize_skills(skills):
    """
    Приводит навыки к каноническому формату:
    - lowercase + strip
    - применяет SKILL_SYNONYMS для приведения к стандартным названиям
    """
    if not skills:
        return []

    if isinstance(skills, str):
        skills = [skills]

    normalized = []
    for skill in skills:
        s = str(skill).lower().strip()
        canonical = SKILL_SYNONYMS.get(s, s)
        normalized.append(canonical)

    return normalized


def normalize_role(role):
    """Приводит варианты названия роли к единому стандарту."""
    if not role:
        return None
    role = str(role).lower().strip()
    return ROLE_SYNONYMS.get(role, role)


def get_all_role_skills(role):
    """Возвращает плоский словарь всех навыков роли с их баллами."""
    skills_data = ROLE_SKILLS[role]
    all_skills = {}
    all_skills.update(skills_data["critical"])
    all_skills.update(skills_data["main"])
    all_skills.update(skills_data["additional"])
    return all_skills


def calculate_role_score(role, candidate_skills):
    """
    Считает балл кандидата по конкретной роли.
    Возвращает кортеж: (итоговый балл, критических_набрано, критических_всего, отсутствующие_критические)
    """
    skills_data = ROLE_SKILLS[role]
    critical_skills = skills_data["critical"]
    all_skills = get_all_role_skills(role)

    candidate_skills_set = set(candidate_skills)

    # Сумма баллов за все совпавшие навыки
    raw_score = 0
    for skill in candidate_skills_set:
        if skill in all_skills:
            raw_score += all_skills[skill]

    # Подсчёт критических: сколько баллов из критических набрано
    critical_total = sum(critical_skills.values())
    critical_obtained = sum(
        points for skill, points in critical_skills.items()
        if skill in candidate_skills_set
    )

    # Отсутствующие критические навыки
    missing_critical = [
        skill for skill in critical_skills
        if skill not in candidate_skills_set
    ]

    # Hard-cutoff: если не покрыт хотя бы один критический навык - роль выпадает
    if missing_critical:
        final_score = 0
    else:
        final_score = raw_score

    return final_score, critical_obtained, critical_total, missing_critical


def apply_salary_penalty(score, role, salary_expectation, experience_years):
    """
    Корректирует балл по роли с учётом зарплатных ожиданий.
    Если кандидат просит больше senior-вилки роли - штраф -10 баллов.
    Если попадает в нужную вилку по опыту - бонус +3.
    """
    try:
        salary = float(salary_expectation)
    except (TypeError, ValueError):
        return score, "не указана"

    # Если зарплата пришла в рублях (большое число), переводим в тысячи
    if salary > 10000:
        salary = salary / 1000

    try:
        exp = float(experience_years)
    except (TypeError, ValueError):
        exp = 0

    junior_max, middle_max, senior_max = SALARY_RANGES[role]

    # Определяем ожидаемый уровень кандидата по опыту
    if exp < 1:
        expected_max = junior_max
        level = "junior"
    elif exp < 3:
        expected_max = middle_max
        level = "middle"
    else:
        expected_max = senior_max
        level = "senior"

    # Штраф если просит сильно больше своей вилки
    if salary > expected_max * 1.2:
        return max(0, score - 10), f"завышены для {level}"

    # Бонус если попадает в свою вилку
    if salary <= expected_max:
        return score + 3, f"адекватны для {level}"

    return score, f"немного выше {level}-вилки"


def calculate_all_scores(skills, experience_years, salary_expectation):
    """
    Считает баллы по всем ролям с учётом зарплаты и опыта.
    Возвращает dict {роль: {score, critical_obtained, critical_total, missing_critical, salary_note}}
    """
    normalized_skills = normalize_skills(skills)

    try:
        exp = float(experience_years)
    except (TypeError, ValueError):
        exp = 0

    # Бонус за опыт: +2 за 1+ лет, +5 за 3+ лет (умеренно, чтобы не перебить навыки)
    if exp >= 3:
        exp_bonus = 5
    elif exp >= 1:
        exp_bonus = 2
    else:
        exp_bonus = 0

    results = {}
    for role in ROLE_SKILLS:
        score, crit_obt, crit_total, missing = calculate_role_score(role, normalized_skills)

        # Если роль провалила cutoff по критическим - не начисляем бонусы
        if score == 0:
            salary_note = "не учитывается"
        else:
            score += exp_bonus
            score, salary_note = apply_salary_penalty(score, role, salary_expectation, exp)

        score = min(100, max(0, round(score)))

        results[role] = {
            "score": score,
            "critical_obtained": crit_obt,
            "critical_total": crit_total,
            "missing_critical": missing,
            "salary_note": salary_note,
        }

    return results


def get_skills_to_improve(role, candidate_skills, top_n=5):
    """Возвращает список главных навыков, которых не хватает кандидату для роли."""
    candidate_set = set(candidate_skills)
    all_skills = get_all_role_skills(role)

    missing = [
        (skill, points) for skill, points in all_skills.items()
        if skill not in candidate_set
    ]
    missing.sort(key=lambda x: -x[1])

    return [skill for skill, _ in missing[:top_n]]


def compare_desired_and_best_role(desired_role, best_role):
    """Сравнивает желаемую роль с лучшей по скорингу."""
    if not desired_role:
        return "Желаемая роль не указана, рекомендация построена по навыкам и опыту."

    # desired_role уже нормализована перед вызовом - проверяем, попала ли в стандартные роли
    if desired_role in ROLE_SKILLS:
        if desired_role == best_role:
            return f"Вы указали роль «{desired_role}», и она совпадает с нашей рекомендацией."
        return (
            f"Вы указали роль «{desired_role}», но по навыкам и опыту больше подходит «{best_role}»."
        )

    return (
        f"Вы указали роль «{desired_role}», но бот не смог сопоставить её "
        f"с одной из стандартных ролей. Рекомендация построена по навыкам."
    )


def build_feedback(results, normalized_skills, desired_role, role_comment):
    """Формирует итоговый ответ для кандидата."""
    best_role = max(results, key=lambda r: results[r]["score"])
    best_score = results[best_role]["score"]
    best_data = results[best_role]

    # Если ни одна роль не прошла cutoff - кандидат не подходит вовсе
    if best_score == 0:
        score_lines = []
        for role, data in results.items():
            missing = ", ".join(data["missing_critical"])
            score_lines.append(f"• {role}: не хватает критических навыков ({missing})")
        score_details = "\n".join(score_lines)

        return (
            "❌ К сожалению, вы не подходите ни на одну из ролей в ML-команде — "
            "не покрыты критические навыки.\n\n"
            f"Что не хватает по каждой роли:\n{score_details}\n\n"
            "Рекомендуем начать с базовых навыков выбранного направления "
            "(SQL, Python, статистика, основы ML или управление проектами).\n\n"
            f"{role_comment}"
        )

    # Определяем общий вердикт
    if best_score >= 70:
        decision = f"🏆 Отлично подходишь на роль «{best_role}» — {best_score} баллов"
        level = "высокий"
    elif best_score >= 45:
        decision = f"✅ Подходишь на роль «{best_role}» — {best_score} баллов"
        level = "средний"
    else:
        decision = f"⚠️ Частично подходишь на роль «{best_role}» — {best_score} баллов"
        level = "ниже среднего"

    # Детализация по всем ролям
    score_lines = []
    for role, data in sorted(results.items(), key=lambda x: -x[1]["score"]):
        if data["score"] == 0:
            missing = ", ".join(data["missing_critical"])
            score_lines.append(f"• {role}: не рассматривается (нет: {missing})")
        else:
            score_lines.append(f"• {role}: {data['score']} баллов")
    score_details = "\n".join(score_lines)

    # Что подкачать
    to_improve = get_skills_to_improve(best_role, normalized_skills, top_n=5)
    improve_note = (
        f"🔧 Подкачать для роли «{best_role}»: {', '.join(to_improve)}"
        if to_improve else ""
    )

    # Комментарий по зарплате
    salary_note = f"💰 Зарплатные ожидания: {best_data['salary_note']}"

    parts = [
        decision,
        "",
        f"Уровень соответствия: {level}",
        "",
        f"Баллы по всем ролям:\n{score_details}",
        "",
        "✅ Все критические навыки в порядке",
        salary_note,
    ]

    if improve_note:
        parts.append(improve_note)

    parts.append("")
    parts.append(role_comment)

    return "\n".join(parts)


class ActionEvaluateCandidate(Action):
    """
    Кастомное действие RASA: получает данные из слотов,
    считает баллы по всем ролям с учётом навыков, опыта и зарплаты,
    отправляет кандидату итоговую рекомендацию.
    """

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
        desired_role = tracker.get_slot("desired_role")

        desired_role = normalize_role(desired_role)
        normalized_skills = normalize_skills(skills)

        results = calculate_all_scores(skills, experience_years, salary_expectation)

        best_role = max(results, key=lambda r: results[r]["score"])
        role_comment = compare_desired_and_best_role(desired_role, best_role)

        feedback = build_feedback(results, normalized_skills, desired_role, role_comment)

        dispatcher.utter_message(text=feedback)

        return []
