from prettytable import from_db_cursor

from hh_employers_database.config import config
from hh_employers_database.dbmanager import DBManager
from hh_employers_database.hh_api import HeadHunterAPI
from hh_employers_database.utils import filling_database, execute_sql_script

hh_api = HeadHunterAPI()
script_file = 'queries.sql'
db_name = 'my_new_db'
params = config()
psql = DBManager(db_name, params)


def main():
    execute_sql_script(psql.cursor, script_file)
    data = hh_api.get_vacancies_by_employers()
    filling_database(psql, data)

    psql.cursor = psql.connection.cursor()
    while True:
        try:
            user_input = int(input('Выберите действие:\n'
                                   '1 - Получить список всех компаний и количество вакансий у каждой компании\n'
                                   '2 - Получить список всех вакансий\n'
                                   '3 - Получить среднюю зарплату по вакансиям\n'
                                   '4 - Получить список всех вакансий, у которых зарплата '
                                   'выше средней по всем вакансиям\n'
                                   '5 - Получить список всех вакансий, в названии которых содержится переданное '
                                   'ключевое слово'
                                   '\n6 - Закончить работу с базой данных\n'))
        except ValueError:
            print('Это не цифра, попробуй еще раз\n')
            continue
        if user_input == 1:
            psql.get_companies_and_vacancies_count()
            table = from_db_cursor(psql.cursor)
            print(table)
        elif user_input == 2:
            psql.get_all_vacancies()
            table = from_db_cursor(psql.cursor)
            print(table)
        elif user_input == 3:
            result = psql.get_avg_salary()
            print(f'Средня зарплата по вакансиям составляет: {result[0]} {result[1]}')
        elif user_input == 4:
            psql.get_vacancies_with_higher_salary()
            table = from_db_cursor(psql.cursor)
            print(table)
        elif user_input == 5:
            user_word = input('Введите слово для поиска:\n')
            psql.get_vacancies_with_keyword(user_word)
            table = from_db_cursor(psql.cursor)
            print(table)
        elif user_input == 6:
            psql.close_cursor()
            psql.close_connection()
            print('Программа закончена.')
            print('База данных закрыта')
            break
        else:
            print("Такого действия нет, попробуйте еще раз")


if __name__ == '__main__':
    main()
