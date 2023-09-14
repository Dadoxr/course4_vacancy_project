import os
from src.utils import *


def main():
    employers = {
        '3529': "Сбер", 
        '78638': "Тинькофф", 
        '4181': "ВТБ", 
        '1122462': "Skyeng",
        '9352463': "X5",
        '12550': "ПИК",
        '1740': "Яндекс",
        '4949': "P&G",
        '10122709': "Uptrade",
        '2863076': "Skillbox"
    }
    # Создание или обновление базы вакансий
    text = input('Введи ключевые слова для парсинга вакансий: ')
    employers_id = input(f'Введи id компаний через пробел или остальте пустым(по умолчанию {", ".join(list(employers.values()))}): ')
    
    try:
        employers_id = [str(int(i)) for i in employers_id.split(' ')] if employers_id else list(employers.keys())
    except ValueError:
        print('Вы ввели не числа или не через пробел. Запустите скрипт заново')
        return
    except Exception as e:
        print(f'Остановка из-за ошибки: {e}. \n\nЗапустите скрипт заново')
        return

    
    print('Запуск парсинга')    
    db = renew_vacancy(text, employers_id)
    print('Парсинг окончен')


    # Запуск безпрерывной работы со списком для пользователя
    while True:
        
        # Запрос пользователю на фильтр вакансий
        action = input(
'''
Выбирите дополнительные действия: 
1 - Получить список всех компаний и количество вакансий у каждой компании., 

2 - Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.

3 - Получить среднюю зарплату по вакансиям.

4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.

5 - Получить список всех вакансий, в названии которых содержатся переданные слова (надо будет ввести слова).

CTRL+C - закончить


''')    
        results = None
        if action == '1':
            results = db.get_employers_and_vacancies_count() or 'Нет результата'
        elif action == '2':
            results = db.get_all_vacancies() or 'Нет результата'
        elif action == '3':
            print(f'Cредняя зарплата составляет: {db.get_avg_salary()} руб')
        elif action == '4':
            results = db.get_vacancies_with_higher_salary() or 'Нет результата'
        elif action == '5':
            keywords = input('Введите слова через пробел: ' ).split(' ')
            results = db.get_vacancies_with_keyword(keywords) or 'Нет результата'
        else:
            print('Неизвестная комбинация, попробуйте еще раз')

        if results:
            for result in results:
                print(result)
                print()
        continue


if __name__ == "__main__":
    main()


