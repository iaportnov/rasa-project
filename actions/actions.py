from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sys
import os
import re

# Добавляем текущую папку в путь, чтобы RASA видел наши модули
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skills_config import skills_weights, skill_to_skill, CRITICAL_SKILLS, ROLE_SALARY_RANGES
from embeddings import extract_skills
from scoring import simple_scoring
from dijkstra_module import dijkstra_scoring

import networkx as nx

# ====================== GRAPH ======================
G = nx.Graph()
roles = ['project_manager', 'data_analyst', 'data_engineer', 'data_scientist', 'mlops_engineer']

role_names_ru = {
    'project_manager': 'Менеджер проекта',
    'data_analyst': 'Дата-аналитик',
    'data_engineer': 'Дата-инженер',
    'data_scientist': 'Дата-сайентист',
    'mlops_engineer': 'MLOps-инженер'
}

# Маппинг для распознавания ролей из текста
ROLE_SYNONYMS = {
    'project_manager': ['пм', 'менеджер', 'project', 'управление', 'pm', 'проектами'],
    'data_analyst': ['аналитик', 'analyst', 'da', 'аналитика', 'дата аналитик'],
    'data_engineer': ['инженер', 'engineer', 'de', 'инженерия', 'дата инженер'],
    'data_scientist': ['сайентист', 'scientist', 'ds', 'наука', 'дс', 'дата сайентист'],
    'mlops_engineer': ['мл', 'млпс', 'mlops', 'ml ops', 'млопс']
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
        return 'validate_vacancy_form'

    def validate_preferred_role(self, slot_value, dispatcher, tracker, domain):
        text = str(slot_value).lower()
        
        any_words = ['любая', 'нет', 'не важно', 'все', 'всё', 'не имею', 'любую', 'без разницы']
        if any(word in text for word in any_words):
            return {'preferred_role': 'any'}
        
        # Ищем совпадения по синонимам ролей
        for role, synonyms in ROLE_SYNONYMS.items():
            if any(syn in text for syn in synonyms):
                dispatcher.utter_message(text=f'👌 Понял, рассматриваем вас на позицию: {role_names_ru[role]}.')
                return {'preferred_role': role}
        
        dispatcher.utter_message(text='Не совсем понял роль. Можете уточнить или написать "любая"?')
        return {'preferred_role': None}

    def validate_experience_years(self, slot_value, dispatcher, tracker, domain):
        nums = re.findall(r'\d+\.?\d*', str(slot_value))
        if nums:
            return {'experience_years': float(nums[0])}
        return {'experience_years': None}

    def validate_skills(self, slot_value, dispatcher, tracker, domain):
        if tracker.get_slot('requested_slot') != 'skills':
            return {}
        
        accumulated = tracker.get_slot('skills_accumulated') or []
        user_text = tracker.latest_message.get('text', '').lower()
        
        # --- Удаление ---
        remove_words = ['удали', 'убери', 'исключи', 'минус', 'удалить', 'убрать']
        if any(word in user_text for word in remove_words):
            skills_to_delete = extract_skills(user_text)
            to_remove = [s for s in skills_to_delete if s in accumulated]
            if to_remove:
                accumulated = [s for s in accumulated if s not in to_remove]
                dispatcher.utter_message(text=f'🗑 Убрал: {", ".join(to_remove)}. \n📋 Осталось: {", ".join(accumulated) if accumulated else "пусто"}')
                return {'skills': None, 'skills_accumulated': accumulated}
            return {'skills': None, 'skills_accumulated': accumulated}

        # --- Завершение ---
        stop_words = ['все', 'всё', 'конец', 'хватит', 'готово', 'закончил']
        if any(word in user_text for word in stop_words):
            if not accumulated:
                dispatcher.utter_message(text='Сначала напишите свои навыки!')
                return {'skills': None}
            return {'skills': accumulated, 'skills_accumulated': accumulated}
        
        # --- Добавление ---
        new_skills = list(extract_skills(user_text).keys())
        added = []
        for s in new_skills:
            if s not in accumulated:
                accumulated.append(s)
                added.append(s)
        
        if added:
            dispatcher.utter_message(text=f'👍 Добавил: {", ".join(added)}. \n📋 Сейчас в списке: {", ".join(accumulated)}. (Напишите "всё", если это всё)')
        else:
            dispatcher.utter_message(text='Не распознал навыки. Попробуйте еще раз или напишите "всё".')
            
        return {'skills': None, 'skills_accumulated': accumulated}

    def validate_salary_expected(self, slot_value, dispatcher, tracker, domain):
        nums = re.findall(r'\d+', str(slot_value))
        if nums:
            return {'salary_expected': float(nums[0])}
        dispatcher.utter_message(text='Пожалуйста, введите желаемую зарплату числом.')
        return {'salary_expected': None}


class ActionEvaluateCandidate(Action):
    def name(self) -> Text:
        return 'action_evaluate_candidate'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        preferred_role = tracker.get_slot('preferred_role')
        skills_list = tracker.get_slot('skills') or []
        exp_years = float(tracker.get_slot('experience_years') or 0)
        salary_expected = float(tracker.get_slot('salary_expected') or 0)
        
        skill_map = extract_skills(' '.join(skills_list))
        
        scoring_scores = simple_scoring(skill_map, roles)
        dijkstra_scores = dijkstra_scoring(G, skill_map, roles)

        final_scores = {}
        # Определяем, какие роли оценивать
        roles_to_evaluate = [preferred_role] if preferred_role and preferred_role != 'any' else roles

        for role in roles_to_evaluate:
            skill_score = (scoring_scores.get(role, 0) + dijkstra_scores.get(role, 0)) / 2
            exp_bonus = min(exp_years * 15, 100)
            salary_bonus = 0
            rng = ROLE_SALARY_RANGES.get(role, {'min': 0, 'max': 999999})
            if rng['min'] <= salary_expected <= rng['max']:
                salary_bonus = 50
            
            final_scores[role] = round(skill_score + exp_bonus + salary_bonus)

        # Если пользователь выбрал конкретную роль
        if preferred_role and preferred_role != 'any':
            target_role = preferred_role
            critical = CRITICAL_SKILLS.get(target_role, [])
            missing_critical = [s for s in critical if s not in skill_map]
            salary_limit = ROLE_SALARY_RANGES[target_role]['max'] * 3
            is_salary_too_high = salary_expected > salary_limit

            if missing_critical:
                text = f'❌ К сожалению, вы не подходите на желаемую позицию {role_names_ru[target_role]}\n\n'
                text += f'Причина: Отсутствуют критически важные навыки: {", ".join(missing_critical)}.'
            elif is_salary_too_high:
                text = f'❌ Отказ по позиции {role_names_ru[target_role]}\n\n'
                text += f'Причина: Ваши зарплатные ожидания значительно выше бюджета для этой роли.'
            else:
                text = f'✅ Отличные новости! Вы подходите на позицию {role_names_ru[target_role]}!\n\n'
                text += f'Ваш профиль соответствует нашим требованиям для этой вакансии.'
            
            best_role = target_role
        else:
            # Общий скоринг
            best_role = max(final_scores, key=final_scores.get)
            text = f'🏆 На основе ваших навыков, лучшая роль — {role_names_ru[best_role]}!\n\n'
            text += '📈 Ваша релевантность ролям:\n'
            sorted_roles = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
            for role, score in sorted_roles:
                text += f'• {role_names_ru[role]}\n'

        # План развития
        missing_skills = [s for s in skills_weights if s not in skill_map and G.has_edge(s, best_role)]
        if missing_skills:
            missing_skills.sort(key=lambda x: skills_weights[x].get(best_role, 0), reverse=True)
            top_missing = missing_skills[:3]
            text += f'\n\n🔧 Рекомендация для роста в роли {role_names_ru[best_role]}:\n'
            text += f'Изучите {", ".join(top_missing)}, это значительно усилит ваше резюме.'

        dispatcher.utter_message(text=text)
        return [SlotSet('skills_accumulated', None), SlotSet('skills', None), SlotSet('salary_expected', None), SlotSet('experience_years', None), SlotSet('preferred_role', None)]


class ActionShowCandidateData(Action):
    def name(self) -> Text:
        return 'action_show_candidate_data'
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text='Оценка завершена.')
        return []