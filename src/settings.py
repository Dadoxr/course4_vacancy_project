import dotenv, os

dotenv.load_dotenv()


SUPERJOB_SECRET_KEY = os.getenv('SUPERJOB_SECRET_KEY')

VACANCY_FILENAME = 'vacancies.json'

CURRENCY_URL = 'https://www.cbr.ru/currency_base/daily/'
