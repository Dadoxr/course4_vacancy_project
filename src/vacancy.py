

class Vacancy:

    def __init__(self, title, link, salary_from, salary_to, salary_currency, requirements):
        self.title = title
        self.link = link
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.requirements = requirements

        
    def __gt__(self, other):
        '''Сравнение больше по зарплате'''
        return self.salary_from > other.salary_from