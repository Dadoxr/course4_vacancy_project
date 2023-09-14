import os, sys, psycopg2
sys.path.append(os.getcwd())

from classes.base import BaseSaveClass
from src.settings import DB_COMP_TABLE_NAME, DB_NAME, DB_PARAMS, DB_VAC_TABLE_NAME


class DBSaver(BaseSaveClass):
    is_connected = False

    def __init__(self) -> None:
        if not self.is_connected:
            delete_db_query  = f'''DROP DATABASE IF EXISTS {DB_NAME}'''
            create_db_query = f'''CREATE DATABASE {DB_NAME}'''
            create_vac_table_query = f'''
                CREATE TABLE IF NOT EXISTS {DB_VAC_TABLE_NAME}' (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255),
                    company_id INTEGER REFERENCES {DB_COMP_TABLE_NAME}(id),
                    link TEXT,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    salary_currency VARCHAR(50),
                    requirements TEXT
                    )
            '''
            create_emp_table_query = f'''
                CREATE TABLE IF NOT EXISTS {DB_COMP_TABLE_NAME}' (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(255),
                    link TEXT,
                    description TEXT
                    )
            '''
            conn = psycopg2.connect(**DB_PARAMS, dbname = 'postgres')
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(delete_db_query)
            cur.execute(create_db_query)
            cur.close()
            conn.close()

            self.conn = psycopg2.connect(**DB_PARAMS, dbname = DB_NAME)
            self.conn.autocommit = True
            with self.conn.cursor() as cur:
                cur.execute(create_vac_table_query)
                cur.execute(create_emp_table_query)

            self.is_connected = True


    def add_vacancy(self, vacancy: object) -> None:
        '''Добавление вакансии в таблицу'''

        with self.conn.cursor() as cur:
            cur.execute(f'INSERT INTO {DB_VAC_TABLE_NAME} ')


    def delete_vacancy(self, vacancy: object) -> None:
        '''Удаление вакансии из таблицы'''
        
        with self.conn.cursor() as cur:
            cur.execute(f'DELETE FROM {DB_VAC_TABLE_NAME} WHERE id = {vacancy.id}')
    

    def get_companies_and_vacancies_count(self) -> list[object | None]:
        '''получает список всех компаний и количество вакансий у каждой компании.'''
        
        query = f'''
            SELECT comp.*, COUNT(vac.*) count_vac
            FROM {DB_COMP_TABLE_NAME} comp
            INNER JOIN {DB_VAC_TABLE_NAME} vac
                ON vac.company_id = comp.id
            GROUP BY comp.*
            ORDER BY comp.name
        '''
        with self.conn.cursor() as cur:
            cur.execute(query)
        
        return cur.fetchall()


    def get_all_vacancies(self) -> list[object | None]:
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.'''
        
        query = f'''
            SELECT vac.title, comp.name, vac.salary_from, vac.salary_to, vac.salary_currency, vac.link
            FROM {DB_VAC_TABLE_NAME} vac
            INNER JOIN {DB_COMP_TABLE_NAME} comp
                ON vac.company_id = comp.id
            ORDER BY vac.salary_to
        '''
        
        with self.conn.cursor() as cur:
            cur.execute(query)
        
        return cur.fetchall()


    def get_avg_salary(self) -> int:
        '''получает среднюю зарплату по вакансиям.'''
        
        query = f'''
            SELECT AVG(salary_to) average_salary
            FROM {DB_VAC_TABLE_NAME}
        '''

        with self.conn.cursor() as cur:
            cur.execute(query)
        
        return cur.fetchall()


    def get_vacancies_with_higher_salary(self) -> list[object | None]:
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.'''
        
        query = f'''
            SELECT * 
            FROM {DB_VAC_TABLE_NAME} WHERE salary_from >
                (SELECT AVG(salary_to) average_salary
                 FROM {DB_VAC_TABLE_NAME})
        '''
        
        with self.conn.cursor() as cur:
            cur.execute(query)
        
        return cur.fetchall()


    def get_vacancies_with_keyword(self, filter_words: list=None) -> list[object | None]:
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.'''
        
        if filter_words:
            query = f'''
                SELECT * 
                FROM {DB_VAC_TABLE_NAME}
                WHERE title LIKE %{filter_words[0]}% '
            '''
            if len(filter_words) > 1:
                for word in filter_words[1:]:
                    query += f' OR title LIKE %{word}%'
        else:
            query = f'''
                SELECT * 
                FROM {DB_VAC_TABLE_NAME}
            '''


        with self.conn.cursor() as cur:
            cur.execute(query)
        
        return cur.fetchall()
