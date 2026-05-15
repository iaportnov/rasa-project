# scoring.py
from skills_config import skills_weights

def simple_scoring(candidate_skills, roles):
    scores = {}
    
    for role in roles:
        total = 0
        relevant_count = 0
        
        for skill in candidate_skills:
            weight = skills_weights.get(skill, {}).get(role, 0)
            if weight > 0:
                total += weight
                relevant_count += 1
        
        if relevant_count == 0:
            scores[role] = 0
        else:
            base_score = total * 12 
            bonus = relevant_count * 5
            scores[role] = min(100, base_score + bonus)
    
    return scores
