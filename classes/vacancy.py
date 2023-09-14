class Vacancy:

    vacancy_list = []
    
    def __init__(self, id, title, link, salary_from, salary_to, salary_currency, requirements):
        self.id = id
        self.title = title
        self.link = link
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.requirements = requirements

    
    def __repr__(self):
        return '''%s(id=%s, title=%s, link=%s, salary_from=%s, salary_to=%s, salary_currency=%s, requirements=%s)''' % (
            self.__class__.__name__, self.title, self.link, self.salary_from, self.salary_to, self.salary_currency, self.requirements
        )
    
    
    def __gt__(self, other):
        '''Сравнение больше по ЗП(от)'''

        return self.salary_from > other.salary_from