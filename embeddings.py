# embeddings.py
from sentence_transformers import SentenceTransformer, util
import torch
import re
from skills_config import SKILL_SYNONYMS, skills_weights

embedder = SentenceTransformer('all-MiniLM-L6-v2')
known_skills = list(skills_weights.keys())

PROFICIENCY_LEVELS = {
    "expert": 1.6, "отлично": 1.6, "хорошо": 1.4, "много": 1.4,
    "advanced": 1.4, "good": 1.3,
    "intermediate": 1.0, "normal": 1.0,
    "beginner": 0.6, "немного": 0.6, "чуть": 0.5, "слабо": 0.5,
    "little": 0.5, "basic": 0.5, "junior": 0.6,
}

def get_proficiency_multiplier(text: str) -> float:
    text_lower = text.lower()
    for word, mult in PROFICIENCY_LEVELS.items():
        if word in text_lower:
            return mult
    return 1.0

def extract_skills(user_text: str):
    """Возвращает dict: skill -> multiplier"""
    if not user_text or not user_text.strip():
        return {}
    
    chunks = re.split(r'[,\s]+и\s+|[,\s]+с\s+|[,\s]+', user_text.lower())
    chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 1]
    
    skill_map = {}
    
    for chunk in chunks:
        multiplier = get_proficiency_multiplier(chunk)
        
        found = False
        for main_skill, synonyms in SKILL_SYNONYMS.items():
            if any(s in chunk for s in synonyms):
                skill_map[main_skill] = max(skill_map.get(main_skill, 0.0), multiplier)
                found = True
                break
        
        if not found:
            user_emb = embedder.encode(chunk, convert_to_tensor=True)
            known_embs = embedder.encode(known_skills, convert_to_tensor=True)
            cos_scores = util.cos_sim(user_emb, known_embs)[0]
            top_idx = torch.argmax(cos_scores).item()
            score = cos_scores[top_idx].item()
            
            if score >= 0.45:
                skill = known_skills[top_idx]
                skill_map[skill] = max(skill_map.get(skill, 0.0), multiplier)
    
    return skill_map