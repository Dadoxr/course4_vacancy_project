import os
from src.utils import *
from src.settings import VACANCY_FILENAME
from classes.jsonsaver import JSONSaver


def main():

    # Создание или обновление базы вакансий
    if os.path.exists(VACANCY_FILENAME):
        is_need_update = input("Нужно обновить вакансии? 1 - да, оставное - нет: ")
        if is_need_update == '1':
            text = input('Введи ключевые слова для парсинга вакансий: ')

            os.remove(VACANCY_FILENAME)
            renew_vacancy(text)
    else:
        text = input('Введи ключевые слова для парсинга вакансий: ')
        renew_vacancy(text)

    # Запрос пользователю на фильтр вакансий
    top_n = input("Введите количество вакансий для вывода в топ N: ")
    sorting_type = input("Введите тип сортировки: 1 - по названию, 2 - по ЗП: ")
    filter_words = input("Введите ключевые слова для фильтрации вакансий(оставьте пустым если нужны все): ").lower()
    salary = input("Введите ЗП от и до. Пример 100000 150000(оставьте пустым если нужны все): ")
    
    # Формативание ответов пользователя и запуск фильтрации и сортировки
    try:
        top_n = int(top_n)
        sorting_type = int(sorting_type)
        filter_words = None if filter_words == '' else filter_words
        salary = [int(i) for i in salary.split()] if salary else None
    except ValueError as e:
        print(f'Вы введи неверные данные. Ошибка ==> {e}')
    else:
        filtered_vacancies = filter_vacancies(filter_words, salary)

        if not filtered_vacancies:
            print("Нет вакансий, соответствующих заданным критериям. Запистите заново")
            return

        sorted_vacancies = sort_vacancies(sorting_type, filtered_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
        print_vacancies(top_vacancies)

        # Запуск безпрерывной работы со списком для пользователя
        while True:
            action = input("Выбирите дополнительные действия: 1 - Удалить ваканцию, CTRL+C - закончить: ")
            
            if action == '1':
                vacancy_id = input('Напишите ID вакансии: ')
                
                if vacancy_id.isdigit():
                    JSONSaver.delete_vacancy(top_vacancies, int(vacancy_id))
                    print('Вакансия удалена')
                    print_vacancies(top_vacancies)
                else:
                    print('Вы ввели не число')
            else:
                print('Нет такой опции')
            continue


if __name__ == "__main__":
    main()


