import os, sys

from src.settings import DB_EMP_TABLE_NAME, DB_VAC_TABLE_NAME
sys.path.append(os.getcwd())

from classes.currency import Currency
from classes.headhunterapi import HeadHunterAPI
from classes.vacancy import Vacancy
from classes.dbsaver import DBSaver
from classes.employer import Employer


def renew_vacancy(text, employers_id):

    
    hh_api = HeadHunterAPI()

    print('Начал парсинг HH вакансий')
    hh_vacancies_list = hh_api.get_vacancies(text)
    print('Начал парсинг HH компаний')
    hh_employers_list = hh_api.get_employers(employers_id)

    # Получаем данные всех валют
    print('Начал парсинг валют')
    currency_cite_data = Currency.make_request()

    print('Начал форматировать вакансии и компании в общий вид')
    formated_vacancies = formating_vacancies(hh_vacancies_list, currency_cite_data, employers_id)
    formated_employers = formating_employers(hh_employers_list)
    
    db = DBSaver()
    print('Сохраняю в базу данных')
    db.add(DB_EMP_TABLE_NAME, formated_employers)
    print(f'Компании добавлены в кол-ве {len(formated_employers)}')
    db.add(DB_VAC_TABLE_NAME, formated_vacancies)
    print(f'Вакансии добавлены в кол-ве {len(formated_vacancies)}')
    
    return db


def formating_vacancies(hh_vacancies_list: list[dict], currency_cite_data: str, employers_id: list[str]) -> list[list[object]]:
    print(f'Всего вакансий: {len(hh_vacancies_list)}')
    print('Обработка(точка = 1 вакансия с подходящей компанией):')
    count = 0
    # Формитирования вакансий HH.ru для добавление в DB
    for vacancy in hh_vacancies_list:
        employer_id = str(vacancy.get('employer', {}).get('id', {}))
        if employer_id in employers_id:
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

            Vacancy(id, title, employer_id, link, salary[0], salary[1], salary[2], requirements)
            print('.', end='')
            sys.stdout.flush()
    print('\n')
    return Vacancy.vacancies_list


def formating_employers(hh_employers_list: list[dict]) -> list[list[object]]:
    for hh_employer in hh_employers_list:
        id = hh_employer.get('id', '')
        name = hh_employer.get('name', '')
        link = hh_employer.get('site_url', '')
        description = hh_employer.get('description', '')

        Employer(id, name, link, description)
    return Employer.employers_list


