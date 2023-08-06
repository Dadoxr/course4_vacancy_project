import os, sys, requests
sys.path.append(os.getcwd())

from bs4 import BeautifulSoup
import requests
from .base import BaseAPIClass
from src.settings import CURRENCY_URL


class Currency(BaseAPIClass):
    
    @staticmethod
    def make_request() -> str:
        response = requests.get(CURRENCY_URL)
        data = response.text
        
        return data
    

    @staticmethod
    def get_data(currency: str, data: str) -> float|None:
        '''Форматирование ответа сайта ==> Получение курса валюты'''

        soup = BeautifulSoup(data, 'html.parser')
        table = soup.find('table', class_='data')
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) < 5:
                continue
            if columns[1].text == currency:
                rate = float(columns[4].text.replace(',', '.')) / int(columns[2].text)
                return rate
        return None


    @classmethod
    def convert_to_rub(cls, salary_from: int, salary_to: int, currency: str, data: str) -> (int, int, str):
        '''Конвертация ЗП в рубли'''
        if currency.lower() in ['rur', 'rub'] or (salary_from == 0 and salary_to == 0):
            return salary_from, salary_to, 'RUB'
        
        rate = cls.get_data(currency.upper(), data)
        if rate is not None:
            salary_from = int(salary_from * rate)
            salary_to = int(salary_to * rate)        
        return salary_from, salary_to, 'RUB'