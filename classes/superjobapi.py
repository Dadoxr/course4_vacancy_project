import os, sys, requests
sys.path.append(os.getcwd())

from .base import BaseAPIClass
from src.settings import SUPERJOB_SECRET_KEY


class SuperJobAPI(BaseAPIClass):


    @staticmethod
    def make_request(text: str, page: int) -> dict:
        '''Получения страницы со списком вакансий.'''

        url = 'https://api.superjob.ru/2.0/vacancies/'
        params = {
            'keyword': text,
            'page': page,
            'count': 100
        }
        headers = {'X-Api-App-Id': SUPERJOB_SECRET_KEY}

        vacancies = requests.get(url, params=params, headers=headers)
        return vacancies.json()


    @classmethod
    def get_data(cls, text: str) -> list[dict]:
        '''Получение всех страниц и формирование общего листа с вакансиями'''
        
        page = 0
        vacancies = cls.make_request(text, page)
        num_pages = round(((cls.make_request(text, page))['total'] / 100) + 0.5)

        vacancies_list = []
        while page < num_pages:
            vacancies = cls.make_request(text, page)
            vacancies_list.extend(vacancies['objects'])
            page += 1

        return vacancies_list


