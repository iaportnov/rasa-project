# main.py
from skills_config import skills_weights, skill_to_skill, CRITICAL_SKILLS
from embeddings import extract_skills
from scoring import simple_scoring
from dijkstra_module import dijkstra_scoring

import networkx as nx

print("🚀 Запуск HR-бота — 5 модулей + уровень владения\n")

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
    for role, weight in weights.items():
        G.add_edge(skill, role, weight=weight)

for skill, targets in skill_to_skill.items():
    for target in targets:
        if target in skills_weights:
            G.add_edge(skill, target, weight=1)

# ====================== ЗАПУСК ======================
def evaluate_candidate(skills_text: str):
    print(f"\n🎯 Введено: {skills_text}")
    
    skill_map = extract_skills(skills_text)           # dict: skill → multiplier
    candidate_skills = list(skill_map.keys())
    
    print(f"   Распознано: {candidate_skills}\n")

    if not candidate_skills:
        print("❌ Навыки не распознаны.")
        return

    scoring_scores = simple_scoring(skill_map, roles)
    dijkstra_scores = dijkstra_scoring(G, skill_map, roles)

    final_scores = {}
    for role in roles:
        avg = (scoring_scores[role] + dijkstra_scores[role]) / 2
        final_scores[role] = round(avg)

    best_role = max(final_scores, key=final_scores.get)
    best_score = final_scores[best_role]

    print(f"🏆 ИТОГОВЫЙ РЕЗУЛЬТАТ (среднее): {role_names_ru[best_role]} — {best_score} баллов\n")

    print("Сравнение методов:")
    print("Метод              | Скоринг | Дейкстра | Среднее")
    print("-" * 55)
    for role in roles:
        print(f"{role_names_ru[role]:18} | {scoring_scores[role]:7} | {dijkstra_scores[role]:8} | {final_scores[role]:7}")

    # Критические навыки
    critical = CRITICAL_SKILLS.get(best_role, [])
    missing_critical = [s for s in critical if s not in candidate_skills]
    
    if missing_critical:
        print(f"\n❌ НЕ ПОДХОДИТ — отсутствуют критические навыки: {missing_critical}")
    else:
        print(f"\n✅ ПОДХОДИТ на {role_names_ru[best_role]}")

    missing = [skill for skill in skills_weights if skill not in candidate_skills and G.has_edge(skill, best_role)]
    if missing:
        print(f"\n🔧 Нужно подкачать: {', '.join(missing[:12])}")

if __name__ == "__main__":
    print("="*90)
    print("   ТЕСТЕР HR-БОТА — УРОВЕНЬ ВЛАДЕНИЯ НАВЫКАМИ")
    print("="*90)

    while True:
        text = input("\n👤 Навыки кандидата: ").strip()
        if text.lower() in ["exit", "quit", "выход", ""]:
            break
        evaluate_candidate(text)