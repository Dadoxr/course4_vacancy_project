import os, sys, requests
sys.path.append(os.getcwd())

from .base import BaseAPIClass


class HeadHunterAPI(BaseAPIClass):

    @staticmethod
    def make_request(text: str, page: int) -> dict:
        '''Получения страницы со списком вакансий.'''

        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': f'NAME:{text}',
            'page': page,
            'per_page': 100
        }
        vacancies = requests.get(url, params) 
        return vacancies.json()


    @classmethod
    def get_data(cls, text: str) -> list[dict]:
        '''Получение всех страниц и формирование общего листа с вакансиями'''
        
        page = 0
        vacancies = cls.make_request(text, page)
        num_pages = vacancies['pages']

        vacancies_list = []
        while page < num_pages:
            vacancies = cls.make_request(text, page)
            vacancies_list.extend(vacancies['items'])
            page += 1

        return vacancies_list


