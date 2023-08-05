from dotenv import load_dotenv
import os

load_dotenv()
PROJECT_PATH = os.getcwd()

SUPERJOB_SECRET_KEY = os.getenv('SUPERJOB_SECRET_KEY')

VACANCY_FILENAME = 'vacancies.json'