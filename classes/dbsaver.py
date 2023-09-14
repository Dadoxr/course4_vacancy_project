import os, sys, psycopg2
sys.path.append(os.getcwd())

from classes.base import BaseSaveClass
from src.settings import DB_EMP_TABLE_NAME, DB_NAME, DB_PARAMS, DB_VAC_TABLE_NAME


class DBSaver(BaseSaveClass):
    is_connected = False

    def __init__(self) -> None:
        if not self.is_connected:
            delete_db_query  = f'''DROP DATABASE IF EXISTS {DB_NAME}'''
            create_db_query = f'''CREATE DATABASE {DB_NAME}'''
            create_vac_table_query = f'''
                CREATE TABLE {DB_VAC_TABLE_NAME} (
                    id INTEGER PRIMARY KEY,
                    title VARCHAR(255),
                    employer_id INTEGER REFERENCES {DB_EMP_TABLE_NAME}(id),
                    link VARCHAR,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    salary_currency VARCHAR(50),
                    requirements TEXT
                    )
            '''
            create_emp_table_query = f'''
                CREATE TABLE {DB_EMP_TABLE_NAME} (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(255),
                    link VARCHAR,
                    description TEXT
                    )
            '''
            conn = psycopg2.connect(**DB_PARAMS, dbname = 'postgres')
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(delete_db_query)
            cur.execute(create_db_query)
            print('Пересоздал базу данных')
            cur.close()
            conn.close()

            self.conn = psycopg2.connect(**DB_PARAMS, dbname = DB_NAME)
            self.conn.autocommit = True
            with self.conn.cursor() as cur:
                cur.execute(create_emp_table_query)
                cur.execute(create_vac_table_query)
                print('Создал таблицы с вакансиями и компаниями')

            self.is_connected = True


    def add(self, table_name: str, objs: list[object]) -> None:
        '''Добавление вакансии в таблицу'''

        with self.conn.cursor() as cur:
            columns = ', '.join(list(objs[0].__dict__.keys()))
            values = [tuple(map(str, i.__dict__.values())) for i in objs]

            placeholders = ', '.join(['%s'] * len(list(objs[0].__dict__.keys())))
            sql = f'INSERT INTO "{table_name}" ({columns}) VALUES ({placeholders})'

            cur.executemany(sql, values)



    def delete(self, obj: object, table_name: str) -> None:
        '''Удаление вакансии из таблицы'''
        
        with self.conn.cursor() as cur:
            cur.execute(f'DELETE FROM {table_name} WHERE id = {obj.id}')
    

    def get_employers_and_vacancies_count(self) -> list[object | None]:
        '''получает список всех компаний и количество вакансий у каждой компании.'''
        
        query = f'''
            SELECT emp.id, emp.name, emp.link, emp.description, COUNT(vac.*) count_vac
            FROM {DB_EMP_TABLE_NAME} emp
            INNER JOIN {DB_VAC_TABLE_NAME} vac
                ON vac.employer_id = emp.id
            GROUP BY emp.id, emp.name, emp.link, emp.description
            ORDER BY emp.name
        '''
        with self.conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
        return result


    def get_all_vacancies(self) -> list[object | None]:
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.'''
        
        query = f'''
            SELECT vac.title, emp.name, vac.salary_from, vac.salary_to, vac.salary_currency, vac.link
            FROM {DB_VAC_TABLE_NAME} vac
            INNER JOIN {DB_EMP_TABLE_NAME} emp
                ON vac.employer_id = EMP.id
            ORDER BY vac.salary_to
        '''
        
        with self.conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
        return result


    def get_avg_salary(self) -> int:
        '''получает среднюю зарплату по вакансиям.'''
        
        query = f'''
            SELECT AVG(salary_to) average_salary
            FROM {DB_VAC_TABLE_NAME}
        '''

        with self.conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()
            
        return int(result[0])


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
            result = cur.fetchall()
        return result


    def get_vacancies_with_keyword(self, filter_words: list=None) -> list[object | None]:
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.'''
        
        if filter_words:
            query = f'''
                SELECT * 
                FROM {DB_VAC_TABLE_NAME}
                WHERE title ILIKE '%{filter_words[0]}%'
            '''
            if len(filter_words) > 1:
                for word in filter_words[1:]:
                    query += f" OR title ILIKE '%{word}%'"
        else:
            query = f'''
                SELECT * 
                FROM {DB_VAC_TABLE_NAME}
            '''
        with self.conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
        return result
