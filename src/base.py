from abc import ABC, abstractmethod


class BaseAPIClass(ABC):
    
    @abstractmethod
    def get_vacancies(self):
        pass



class BaseJSONClass(ABC):
    
    @abstractmethod
    def add_vacancy(vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_salary(salary):
        pass

    @abstractmethod
    def delete_vacancy(vacancy):
        pass

