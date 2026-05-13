# dijkstra_module.py
import networkx as nx
from skills_config import skills_weights, skill_to_skill, CRITICAL_SKILLS

def dijkstra_scoring(G, candidate_skills, roles):
    """Исправленный и более чувствительный Дейкстра"""
    scores = {}
    
    print("🔍 Отладка Дейкстры:")
    
    for role in roles:
        temp_G = G.copy()
        source = "candidate_source"
        temp_G.add_node(source)
        
        # Подключаем кандидата ко всем его навыкам
        for skill in candidate_skills:
            if skill in temp_G:
                temp_G.add_edge(source, skill, weight=0)
        
        # Проверка критических навыков
        critical = CRITICAL_SKILLS.get(role, [])
        missing_critical = [s for s in critical if s not in candidate_skills]
        
        if missing_critical:
            scores[role] = 10
            print(f"   {role:18} → критические навыки отсутствуют (штраф)")
            continue
        
        try:
            distance = nx.shortest_path_length(temp_G, source=source, target=role, weight='weight')
            print(f"   {role:18} → расстояние = {distance:.2f}")
        except:
            distance = 999
            print(f"   {role:18} → нет пути")
        
        # Более чувствительная формула
        score = max(0, 100 - int(distance * 28))   # ← увеличил коэффициент
        scores[role] = score
    
    print("-" * 60)
    return scores