import dotenv, os

dotenv.load_dotenv()


SUPERJOB_SECRET_KEY = os.getenv('SUPERJOB_SECRET_KEY')

CURRENCY_URL = 'https://www.cbr.ru/currency_base/daily/'

DB_NAME = 'vacancies_db'
DB_PASSWD = os.getenv('DB_PASSWD')
DB_VAC_TABLE_NAME = 'vacancies'
DB_EMP_TABLE_NAME = 'employers'
DB_PARAMS = {
    'host': 'localhost', 
    'port': 5432, 
    'user': 'postgres', 
    'password': DB_PASSWD
}
