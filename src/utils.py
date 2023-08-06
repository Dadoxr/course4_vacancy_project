import os, sys, json
sys.path.append(os.getcwd())

from classes.currency import Currency
from src.settings import VACANCY_FILENAME
from classes.headhunterapi import HeadHunterAPI
from classes.superjobapi import SuperJobAPI
from classes.vacancy import Vacancy
from classes.jsonsaver import JSONSaver


def filter_vacancies(filter_words: str, salary: list|None) -> list[dict]:
    '''Фильтрация вакансий по словам от пользователя и ЗП'''

    try:
        with open(VACANCY_FILENAME, 'r') as file:
            all_vacancies = json.loads(file.read())
    except FileNotFoundError:
        print(f'{VACANCY_FILENAME} не создан, запусти код заново')
    else:
        filtered_vacancies = all_vacancies
        
        if filter_words is not None:
            filter_words = filter_words.split()
            filtered_vacancies = [vacancy for vacancy in all_vacancies if any(word in vacancy.get('title','').lower() or word in vacancy.get('requirements','').lower() for word in filter_words)]

        if salary is not None:
            filtered_vacancies = [vacancy for vacancy in filtered_vacancies if vacancy.get('salary_from', 0) > salary[0] and vacancy.get('salary_to',0) < salary[1]]
        return filtered_vacancies



def sort_vacancies(sotring_type: int, filtered_vacancies: list[dict]) -> list[dict]:
    '''Сортировка вакансий по ЗП(от) или наименованию'''

    if sotring_type == 1:
        return sorted(filtered_vacancies, key=lambda v: v['title'], reverse=False)
    return sorted(filtered_vacancies, key=lambda v: v['salary_from'], reverse=True)


def get_top_vacancies(filtered_vacancies: list[dict], top_n: int) -> list[dict]:
    '''Выдача первых N вакансий'''

    return filtered_vacancies[:top_n]


def add_vanancies_to_json(text: str) -> None:
    '''Парсинг и добавление вакансий в JSON'''

    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI()
    json_saver = JSONSaver()

    # Получение вакансий с разных платформ
    hh_vacancies_list = hh_api.get_data(text)
    superjob_vacancies_list = superjob_api.get_data(text)
    
    # Получаем данные всех валют
    currency_cite_data = Currency.make_request()
    
    vacancy_list = []

    # Формитирования вакансий HH.ru для дабавление в JSON
    for vacancy in hh_vacancies_list:
        id = vacancy.get('id',0)
        title = vacancy.get('name','Нет названия')
        link = f'''https://hh.ru/vacancy/{id}'''
        requirements_all = vacancy.get('snippet', {})
        requirements = f'''{requirements_all.get('requirement', '')}\n{requirements_all.get('description', '')}'''
        
        salary = vacancy.get('salary') or {}

        salary_from = salary.get('from') or 0 
        salary_to = salary.get('to') or 0
        salary_currency = salary.get('currency') or 'RUR'

        if salary_from != 0 and salary_to == 0:
            salary_to = salary_from
        elif salary_from == 0 and salary_to != 0:
            salary_from = salary_to

        salary = Currency.convert_to_rub(salary_from, salary_to, salary_currency, currency_cite_data)

        vacancy = Vacancy(id, title, link, salary[0], salary[1], salary[2], requirements)

        new_item = {'id': int(vacancy.id),
                    'title': str(vacancy.title), 
                    'link': str(vacancy.link),
                    'salary_from': int(vacancy.salary_from),
                    'salary_to': int(vacancy.salary_to),
                    'salary_currency': str(vacancy.salary_currency),
                    'requirements': str(vacancy.requirements)}
        vacancy_list.append(new_item)

    # Формитирования вакансий superjob для дабавление в JSON
    for vacancy in superjob_vacancies_list:
        id = vacancy.get('id', 0)
        title = vacancy.get('profession', 'Нет названия')
        link = vacancy.get('link', 'Нет ссылки')
        requirements = vacancy.get('candidat', '')

        salary_from = vacancy.get('payment_from') or 0
        salary_to = vacancy.get('payment_to') or 0
        salary_currency = vacancy.get('currency') or 'RUB'

        if salary_from != 0 and salary_to == 0:
            salary_to = salary_from
        elif salary_from == 0 and salary_to != 0:
            salary_from = salary_to

        salary_from = 0 if salary_from is None else salary_from
        salary_to = 0 if salary_to is None else salary_to

        salary = Currency.convert_to_rub(salary_from, salary_to, salary_currency, currency_cite_data)

        vacancy = Vacancy(id, title, link, salary[0], salary[1], salary[2], requirements)

        new_item = {'id': int(vacancy.id),
                    'title': str(vacancy.title), 
                    'link': str(vacancy.link),
                    'salary_from': int(vacancy.salary_from),
                    'salary_to': int(vacancy.salary_to),
                    'salary_currency': str(vacancy.salary_currency),
                    'requirements': str(vacancy.requirements)}
        vacancy_list.append(new_item)

    #Добавление отформатированных вакансий в JSON
    json_saver.add_vacancy(vacancy_list)
    return


def print_vacancies(vacancies):
    for vacancy in vacancies:
        print(f"\
              \nID: {vacancy['id']},\
              \nНазвание: {vacancy['title']},\
              \nСсылка: {vacancy['link']},\
              \nЗарплата: {vacancy['salary_from']} - {vacancy['salary_to']} {vacancy['salary_currency']},\
              \nТребования: {vacancy['requirements']}\n--------------------------------------------------------")


def renew_vacancy(text):
    print('Запуск парсинга')
    add_vanancies_to_json(text)
    print('Парсинг окончен')
    return

