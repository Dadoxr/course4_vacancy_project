class Vacancy:

    vacancies_list = []
    
    def __init__(self, id, title, employer_id, link, salary_from, salary_to, salary_currency, requirements):
        self.id = int(id)
        self.title = str(title)
        self.employer_id = int(employer_id)
        self.link = str(link)
        self.salary_from = int(salary_from)
        self.salary_to = int(salary_to)
        self.salary_currency = str(salary_currency)
        self.requirements = str(requirements)
        self.vacancies_list.append(self)

    
    def __repr__(self):
        return '''%s(id=%s, title=%s, employer_id=%s, link=%s, salary_from=%s, salary_to=%s, salary_currency=%s, requirements=%s)''' % (
            self.__class__.__name__, self.id, self.title, self.employer_id, self.link, self.salary_from, self.salary_to, self.salary_currency, self.requirements
        )
    
    
    def __gt__(self, other):
        '''Сравнение больше по ЗП(от)'''

        return self.salary_from > other.salary_from
    
# a = Vacancy(65, 'title', 5, 'link', 2, 3, 'salary_currency', 'requirements')





