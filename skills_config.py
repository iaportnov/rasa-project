
skills_weights = {
    #Project Manager
    "project_management":   {"project_manager": 5, "data_analyst": 2, "data_engineer": 1, "data_scientist": 1, "mlops_engineer": 1},
    "stakeholder_management":{"project_manager": 5, "data_analyst": 3, "data_engineer": 2, "data_scientist": 2, "mlops_engineer": 2},
    "agile_scrum":          {"project_manager": 5, "data_analyst": 3, "data_engineer": 2, "data_scientist": 2, "mlops_engineer": 2},
    "jira":                 {"project_manager": 5, "data_analyst": 3, "data_engineer": 3, "data_scientist": 2, "mlops_engineer": 3},
    "risk_management":      {"project_manager": 5, "data_analyst": 2, "data_engineer": 2, "data_scientist": 2, "mlops_engineer": 2},
    "roadmap_planning":     {"project_manager": 5, "data_analyst": 3, "data_engineer": 2, "data_scientist": 2, "mlops_engineer": 2},
    "team_leadership":      {"project_manager": 5, "data_analyst": 3, "data_engineer": 2, "data_scientist": 2, "mlops_engineer": 3},
    "business_analysis":    {"project_manager": 4, "data_analyst": 4, "data_engineer": 2, "data_scientist": 2, "mlops_engineer": 2},
    "ml_project_lifecycle": {"project_manager": 4, "data_analyst": 3, "data_engineer": 3, "data_scientist": 4, "mlops_engineer": 4},
    "confluence":           {"project_manager": 4, "data_analyst": 2, "data_engineer": 2, "data_scientist": 2, "mlops_engineer": 2},
    "budgeting":            {"project_manager": 5, "data_analyst": 2, "data_engineer": 1, "data_scientist": 1, "mlops_engineer": 1},

    #Data Analyst
    "sql":                  {"project_manager": 2, "data_analyst": 5, "data_engineer": 4, "data_scientist": 4, "mlops_engineer": 3},
    "python":               {"project_manager": 2, "data_analyst": 5, "data_engineer": 5, "data_scientist": 5, "mlops_engineer": 5},
    "pandas":               {"project_manager": 1, "data_analyst": 5, "data_engineer": 4, "data_scientist": 5, "mlops_engineer": 3},
    "power_bi":             {"project_manager": 1, "data_analyst": 5, "data_engineer": 2, "data_scientist": 3, "mlops_engineer": 2},
    "tableau":              {"project_manager": 1, "data_analyst": 5, "data_engineer": 2, "data_scientist": 3, "mlops_engineer": 2},
    "statistics":           {"project_manager": 2, "data_analyst": 5, "data_engineer": 3, "data_scientist": 5, "mlops_engineer": 3},
    "data_visualization":   {"project_manager": 2, "data_analyst": 5, "data_engineer": 3, "data_scientist": 4, "mlops_engineer": 2},
    "ab_testing":           {"project_manager": 2, "data_analyst": 5, "data_engineer": 2, "data_scientist": 4, "mlops_engineer": 2},

    #Data Engineer
    "etl":                  {"project_manager": 1, "data_analyst": 3, "data_engineer": 5, "data_scientist": 3, "mlops_engineer": 4},
    "spark":                {"project_manager": 1, "data_analyst": 2, "data_engineer": 5, "data_scientist": 4, "mlops_engineer": 4},
    "kafka":                {"project_manager": 1, "data_analyst": 2, "data_engineer": 5, "data_scientist": 3, "mlops_engineer": 5},
    "postgresql":           {"project_manager": 1, "data_analyst": 3, "data_engineer": 5, "data_scientist": 3, "mlops_engineer": 3},
    "clickhouse":           {"project_manager": 1, "data_analyst": 3, "data_engineer": 5, "data_scientist": 3, "mlops_engineer": 4},
    "hadoop":               {"project_manager": 1, "data_analyst": 1, "data_engineer": 4, "data_scientist": 2, "mlops_engineer": 3},
    "data_warehousing":     {"project_manager": 1, "data_analyst": 3, "data_engineer": 5, "data_scientist": 2, "mlops_engineer": 3},
    "dbt":                  {"project_manager": 1, "data_analyst": 3, "data_engineer": 5, "data_scientist": 3, "mlops_engineer": 4},

    #Data Scientist
    "machine_learning":     {"project_manager": 1, "data_analyst": 3, "data_engineer": 2, "data_scientist": 5, "mlops_engineer": 3},
    "scikit_learn":         {"project_manager": 1, "data_analyst": 4, "data_engineer": 3, "data_scientist": 5, "mlops_engineer": 3},
    "pytorch":              {"project_manager": 1, "data_analyst": 3, "data_engineer": 3, "data_scientist": 5, "mlops_engineer": 4},
    "tensorflow":           {"project_manager": 1, "data_analyst": 3, "data_engineer": 3, "data_scientist": 5, "mlops_engineer": 4},
    "deep_learning":        {"project_manager": 1, "data_analyst": 2, "data_engineer": 2, "data_scientist": 5, "mlops_engineer": 4},
    "nlp":                  {"project_manager": 1, "data_analyst": 2, "data_engineer": 2, "data_scientist": 5, "mlops_engineer": 3},
    "computer_vision":      {"project_manager": 1, "data_analyst": 1, "data_engineer": 1, "data_scientist": 5, "mlops_engineer": 3},
    "xgboost":              {"project_manager": 1, "data_analyst": 3, "data_engineer": 2, "data_scientist": 5, "mlops_engineer": 3},

    # MLOps
    "docker":               {"project_manager": 1, "data_analyst": 2, "data_engineer": 4, "data_scientist": 4, "mlops_engineer": 5},
    "kubernetes":           {"project_manager": 1, "data_analyst": 1, "data_engineer": 4, "data_scientist": 4, "mlops_engineer": 5},
    "mlflow":               {"project_manager": 1, "data_analyst": 2, "data_engineer": 4, "data_scientist": 4, "mlops_engineer": 5},
    "monitoring":           {"project_manager": 1, "data_analyst": 2, "data_engineer": 4, "data_scientist": 4, "mlops_engineer": 5},
    "cicd":                 {"project_manager": 2, "data_analyst": 2, "data_engineer": 4, "data_scientist": 4, "mlops_engineer": 5},
    "terraform":            {"project_manager": 1, "data_analyst": 1, "data_engineer": 3, "data_scientist": 3, "mlops_engineer": 5},
}

#КРИТИЧЕСКИЕ НАВЫКИ
CRITICAL_SKILLS = {
    "project_manager": ["project_management", "stakeholder_management", "agile_scrum"],
    "data_analyst":    ["sql", "python", "pandas"],
    "data_engineer":   ["sql", "python", "etl"],
    "data_scientist":  ["machine_learning", "python", "statistics"],
    "mlops_engineer":  ["docker", "kubernetes", "python"],
}

# СИНОНИМЫ
SKILL_SYNONYMS = {
    "project_management": ["управление проектами", "project management", "pm", "проектный менеджмент", "project lead"],
    "stakeholder_management": ["стейкхолдеры", "stakeholder", "управление стейкхолдерами", "заказчики", "stakeholders"],
    "agile_scrum": ["agile", "scrum", "эджайл", "скрам", "agile scrum"],
    "jira": ["джира", "jira", "atlassian jira", "джиру", "jira software"],
    "risk_management": ["управление рисками", "risk management", "риски", "risks", "риск менеджмент"],
    "roadmap_planning": ["роадмап", "roadmap", "планирование роадмапа", "product roadmap", "дорожная карта"],
    "team_leadership": ["лидерство в команде", "team lead", "тимлид", "управление командой", "leadership"],
    "business_analysis": ["бизнес-анализ", "business analysis", "ba", "бизнес аналитик", "business analyst"],
    "ml_project_lifecycle": ["ml lifecycle", "жизненный цикл ml", "ml project lifecycle", "цикл ml проекта", "ml pipeline"],
    "confluence": ["конфлюенс", "confluence", "atlassian confluence", "конфлю", "wiki"],
    "budgeting": ["бюджетирование", "budgeting", "бюджет", "budget management", "финансовое планирование"],

    "sql": ["sql", "sequel", "скуль", "скл", "сел", "postgres", "postgresql"],
    "python": ["питон", "пайтоном", "питончик", "пайтон", "py", "питухон"],

    "pandas": ["пандас", "пандой", "пандос", "pandas", "панда"],
    "power_bi": ["power bi", "powerbi", "павер би", "power bi desktop", "би"],
    "tableau": ["tableau", "табло", "tableau desktop", "таблио", "таблу"],
    "statistics": ["статистика", "statistics", "стат", "статистический анализ", "stats"],
    "data_visualization": ["визуализация данных", "data viz", "датавиж", "data visualization", "дашборды"],
    "ab_testing": ["a/b testing", "a/b тесты", "аб тесты", "ab testing", "сплит тестирование"],

    "etl": ["etl", "elt", "этл", "extract transform load", "data pipeline"],
    "spark": ["spark", "apache spark", "спарк", "pyspark", "spark sql"],
    "kafka": ["kafka", "кафка", "apache kafka", "консьюмер", "producer kafka"],
    "postgresql": ["postgresql", "postgres", "постгрес", "pg", "postgres sql"],
    "clickhouse": ["clickhouse", "кликхаус", "click house", "ch", "clickhouse sql"],
    "hadoop": ["hadoop", "хадуп", "hdfs", "apache hadoop", "hadoop ecosystem"],
    "data_warehousing": ["dwh", "data warehouse", "хранилище данных", "dw", "data warehousing"],
    "dbt": ["dbt", "data build tool", "дбт", "dbt core", "dbt cloud"],

    "machine_learning": ["machine learning", "ml", "машинное обучение", "машин лёрнинг", "ml модели"],
    "scikit_learn": ["scikit-learn", "sklearn", "scikit", "scikit learn", "скикит"],
    "pytorch": ["pytorch", "торч", "питорч", "py torch", "torch"],
    "tensorflow": ["tensorflow", "tf", "тензорфлоу", "tensor flow", "keras"],
    "deep_learning": ["deep learning", "dl", "глубокое обучение", "нейронные сети", "deep nn"],
    "nlp": ["nlp", "natural language processing", "обработка естественного языка", "нлп", "text mining"],
    "computer_vision": ["computer vision", "cv", "компьютерное зрение", "vision", "opencv"],
    "xgboost": ["xgboost", "xgb", "xg boost", "градиентный бустинг", "boosting"],

    "docker": ["docker", "докер", "docker compose", "контейнеры", "dockerfile"],
    "kubernetes": ["kubernetes", "кубер", "k8s", "кубернетес", "k8s cluster"],
    "mlflow": ["mlflow", "ml flow", "млфлоу", "mlops platform", "experiment tracking"],
    "monitoring": ["monitoring", "мониторинг", "prometheus", "grafana", "model monitoring"],
    "cicd": ["ci/cd", "cicd", "continuous integration", "ci cd", "devops pipeline"],
    "terraform": ["terraform", "терраформ", "iac", "infrastructure as code", "tf"],
}

#ЗАРПЛАТНЫЕ ВИЛКИ (в тыс. руб.)
ROLE_SALARY_RANGES = {
    "project_manager": {"min": 150, "max": 350},
    "data_analyst":    {"min": 120, "max": 280},
    "data_engineer":   {"min": 180, "max": 400},
    "data_scientist":  {"min": 200, "max": 450},
    "mlops_engineer":  {"min": 220, "max": 500},
}

#РАСШИРЕННЫЕ СВЯЗИ МЕЖДУ НАВЫКАМИ
skill_to_skill = {
    "python": ["pandas", "numpy", "scikit_learn", "pytorch", "tensorflow", "matplotlib", "seaborn", "xgboost"],
    "pandas": ["numpy", "scikit_learn", "matplotlib", "seaborn", "sql"],
    "sql": ["postgresql", "clickhouse", "etl", "dbt", "data_warehousing"],
    "etl": ["airflow", "kafka", "spark", "dbt"],
    "spark": ["kafka", "hadoop", "etl"],
    "kafka": ["spark", "airflow"],
    "docker": ["kubernetes", "cicd", "terraform", "monitoring"],
    "kubernetes": ["docker", "cicd", "terraform", "mlflow"],
    "pytorch": ["tensorflow", "scikit_learn", "deep_learning", "machine_learning"],
    "tensorflow": ["pytorch", "scikit_learn", "deep_learning"],
    "scikit_learn": ["pandas", "numpy", "xgboost", "machine_learning"],
    "machine_learning": ["scikit_learn", "pytorch", "tensorflow", "deep_learning", "nlp", "computer_vision"],
    "deep_learning": ["pytorch", "tensorflow", "nlp", "computer_vision"],
    "agile_scrum": ["jira", "confluence", "roadmap_planning", "project_management"],
    "jira": ["confluence", "agile_scrum", "roadmap_planning"],
    "project_management": ["agile_scrum", "stakeholder_management", "team_leadership", "risk_management"],
    "mlflow": ["docker", "kubernetes", "cicd", "monitoring"],
    "cicd": ["docker", "kubernetes", "terraform"],
    "monitoring": ["docker", "kubernetes", "mlflow"],
}

__all__ = ["skills_weights", "skill_to_skill", "CRITICAL_SKILLS", "SKILL_SYNONYMS", "ROLE_SALARY_RANGES"]
