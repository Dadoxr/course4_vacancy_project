import os, sys, json 
sys.path.append(os.getcwd())

from src.settings import VACANCY_FILENAME
from .base import BaseJSONClass


class JSONSaver(BaseJSONClass):
    
    
    @staticmethod
    def add_vacancy(vacancies_list: list) -> None:
        '''Добавление листа с вакансиями в JSON'''

        file_content = json.dumps(vacancies_list)
        with open(VACANCY_FILENAME, 'w', encoding="utf-8") as file:
            file.write(file_content)



    @staticmethod
    def delete_vacancy(top_vacancies: list, vacancy_id: int) -> None:
        '''Удаление вакансии по ID их пользовательского листа (не из JSON)'''
        for vacancy in top_vacancies:
            if vacancy.get('id') == vacancy_id:
                top_vacancies.remove(vacancy)



