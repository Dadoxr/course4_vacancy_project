from settings import VACANCY_FILENAME
import json
from base import BaseJSONClass


class JSONSaver(BaseJSONClass):
    
    @staticmethod
    def add_vacancy(vacancy):
        try:
            with open(VACANCY_FILENAME, 'r') as file:
                file_content = file.read()
        except FileNotFoundError:
            with open(VACANCY_FILENAME, 'w') as file:
                file.write(json.dumps([{'title': vacancy.title, 
                                        'link': vacancy.link,
                                        'salary_from': vacancy.salary_from,
                                        'salary_to': vacancy.salary_to,
                                        'salary_currency': vacancy.salary_currency,
                                        'requirement': vacancy.requirement},]))
        else:
            file_list = json.loads(file_content)
            file_list.append({'vacancy': vacancy})
            file_content = json.dumps(file_list)
            with open(VACANCY_FILENAME, 'w') as file:
                file.write(file_content)


    @staticmethod
    def get_vacancies_by_salary(salary):
        pass


    @staticmethod
    def delete_vacancy(vacancy):
        pass



