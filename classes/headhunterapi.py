import os, sys, requests
sys.path.append(os.getcwd())

from classes.base import BaseAPIClass


class HeadHunterAPI(BaseAPIClass):

    @staticmethod
    def make_request(theme: str, params: dict) -> dict:
        '''Получения страницы со списком вакансий.'''
        
        url = f'https://api.hh.ru/{theme}'
        response = requests.get(url, params) 
        return response.json()
    

    @classmethod
    def get_vacancies(cls, text: str) -> list[dict]:
        '''Получение всех страниц и формирование общего листа с вакансиями'''

        print('HH.ru(точка = 100 вакансий):')  
        page = 0
        theme = 'vacancies'
        params = {
            'text': f'NAME:{text}',
            'page': page,
            'per_page': 100
        }
        vacancies = cls.make_request(theme, params)
        num_pages = vacancies['pages']

        vacancies_list = []
        
        while page < num_pages:
            params = {
                'text': f'NAME:{text}',
                'page': page,
                'per_page': 100
            }
            vacancies = cls.make_request(theme, params)
            print('.',end='')
            sys.stdout.flush()
            vacancies_list.extend(vacancies['items'])
            page += 1
        print()
        return vacancies_list


    @classmethod
    def get_employers(cls, employers_id: list) -> list[dict]:
        '''Получение всех страниц и формирование общего листа с вакансиями'''

        employers_list = []

        theme = 'employers'
        for employer_id in employers_id:
            url = f'https://api.hh.ru/{theme}/{employer_id}'
            response = requests.get(url) 
            employer = response.json()
            employers_list.append(employer)
            print(employer.get('name', employer_id), end=', ')
            sys.stdout.flush()
        print()
        return employers_list







