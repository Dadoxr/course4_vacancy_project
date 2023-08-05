from .base import BaseAPIClass
import requests


class HeadHunterAPI(BaseAPIClass):

    @staticmethod
    def get_vacancies(text):
        """
        Получения страницы со списком вакансий.
        """
        
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': f'NAME:{text}',
            'page': 0, # Индекс страницы поиска на HH
            'per_page': 2, # Кол-во вакансий на 1 странице
            #'experience' : 'between1And3', # Опыт работы в годах. noExperience between1And3 between3And6 moreThan6
            #'employment' : 'full', # Тип занятости. full, part, project, volunteer, probation
            # 'salary' : 100000, # 
            #'order_by' : 'publication_time', # сортировка по salary_desc salary_asc relevance distance
            # 'describe_arguments' : True, # Возвращать выбранные параменты поиска?
            # 'responses_count_enabled' : True # Указывать количесво откликов?
        }
        
        vacancies = requests.get(url, params) # Посылаем запрос к API
        vacancies_dict = vacancies.json()
        return vacancies_dict
    

