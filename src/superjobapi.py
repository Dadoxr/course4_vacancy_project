from .base import BaseAPIClass
import requests
from src.settings import SUPERJOB_SECRET_KEY


class SuperJobAPI(BaseAPIClass):

    @staticmethod
    def get_vacancies(text):
        """
        Получения страницы со списком вакансий.
        """

        url = 'https://api.superjob.ru/2.0/vacancies/'
        params = {'keyword': text,}
        headers = {'X-Api-App-Id': SUPERJOB_SECRET_KEY}

        vacancies = requests.get(url, params=params, headers=headers) # Посылаем запрос к API
        vacancies_dict = vacancies.json()
        return vacancies_dict
