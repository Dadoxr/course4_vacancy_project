from settings import VACANCY_FILENAME
import json


def filter_vacancies(filter_words: list[str]) -> list[dict]:
    try:
        with open(VACANCY_FILENAME, 'r') as file:
            all_vacancies = json.loads(file.read())
    except FileNotFoundError:
        print(f'{VACANCY_FILENAME} не создан, запусти parser')
    else:
        filtered_vacancies = [vacancy for vacancy in all_vacancies if any(word in vacancy['title'] or word in vacancy['requirements'] for word in filter_words)]
        return filtered_vacancies



def sort_vacancies(sotring_type: int, filtered_vacancies: list[dict]) -> list[dict]:
    key_value = 'title' if sotring_type == 1 else 'salary_from'
    return sorted(filtered_vacancies, key=lambda v: v[key_value], reverse=True)

def get_top_vacancies(filtered_vacancies, top_n):
    return filtered_vacancies[:top_n]

def print_vacancies():
    pass

