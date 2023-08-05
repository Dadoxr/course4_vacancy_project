import json
from src.headhunterapi import HeadHunterAPI
from src.superjobapi import SuperJobAPI
from src.vacancy import Vacancy
from src.jsonsaver import JSONSaver
from src.utils import *
import os
from src.settings import VACANCY_FILENAME

def add_vanancies_to_json() -> None:
    # Очистка вакансий с файла
    os.remove(VACANCY_FILENAME)
    
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI()
    json_saver = JSONSaver()

    # Получение вакансий с разных платформ
    hh_vacancies = hh_api.get_vacancies("Python")
    superjob_vacancies = superjob_api.get_vacancies("Python")

    # Создание экземпляра класса для работы с вакансиями
    for hh_vacancy in hh_vacancies:
        title = hh_vacancy['items'][0]['id']
        link = f'''https://hh.ru/vacancy/{hh_vacancy['items'][0]['name']}'''
        salary_from = int(f'''{hh_vacancy['items'][0]['salary']['from']}''')
        salary_to = int(f'''{hh_vacancy['items'][0]['salary']['to']}''')
        salary_currency = f'''{hh_vacancy['items'][0]['salary']['currency']}'''
        requirements = hh_vacancy['items'][0]['snippet']['requirement']
        
        vacancy = Vacancy(title, link, salary_from, salary_to, salary_currency, requirements)
        json_saver.add_vacancy(vacancy)

    for sj_vacancy in superjob_vacancies:
        title = sj_vacancy['objects'][0]['profession']
        link = sj_vacancy['objects'][0]['link']
        salary_from = int(f'''{sj_vacancy['objects'][0]['payment_from']} ''')
        salary_to = int(f'''{sj_vacancy['objects'][0]['payment_to']}''')
        salary_currency = f'''{sj_vacancy['objects'][0]['currency']}'''
        requirements = sj_vacancy['objects'][0]['candidat']
        
        vacancy = Vacancy(title, link, salary_from, salary_to, salary_currency, requirements)
        json_saver.add_vacancy(vacancy)
    return


def renew_vacancy():
    print('Запуск обновления вакансий')
    add_vanancies_to_json()
    print('Вакансии обновлены')
    return

# Функция для взаимодействия с пользователем
def user_interaction():
    

        if os.path.exists(VACANCY_FILENAME):
            is_need_update = input("Нужно обновить вакансии? 1 - да, оставное - нет: ")
            if is_need_update == '1':
                renew_vacancy()
        else:
            renew_vacancy()

        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        sorting_type = int(input("Введите тип сортировки: 1 - по названию, 2 - по ЗП "))
        filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
        filtered_vacancies = filter_vacancies(filter_words)

        if not filtered_vacancies:
            print("Нет вакансий, соответствующих заданным критериям.")
            return

        sorted_vacancies = sort_vacancies(sorting_type, filtered_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
        print_vacancies(top_vacancies)
        
        json_saver.get_vacancies_by_salary("100 000-150 000 руб.")
        json_saver.delete_vacancy(vacancy)

if __name__ == "__main__":
    user_interaction()


