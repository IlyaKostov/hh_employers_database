import os
import time
from configparser import ConfigParser

import psycopg2
import requests


class HeadHunterAPI:

    EMPLOYER_ID = ['1740', '15478', '2180', '64174', '84585', '1057', '3776', '3529', '78638', '41862']
    URL_VACANCIES = "https://api.hh.ru/vacancies"
    URL_EMPLOYERS = "https://api.hh.ru/employers/{employer_id}"
    MAX_PAGES = 2

    def get_employers(self):
        employers = []
        for employer in self.EMPLOYER_ID:

            employer_data = requests.get(self.URL_EMPLOYERS.format(employer_id=employer)).json()
            employers.append(employer_data)

            time.sleep(0.25)
        return employers

    def get_vacancies(self):
        """
        Получение списка вакансий с платформы HeadHunter
        :return: list
        """
        vacancies_lst = []
        for employer in self.EMPLOYER_ID:
            for page in range(self.MAX_PAGES):
                params = {'per_page': 2,
                          'page': page,
                          'order_by': "publication_time",
                          'area': [113, 16, 40],
                          'employer_id': employer
                          }
                vacancies = requests.get(self.URL_VACANCIES, params=params).json()
                vacancies_lst.extend(vacancies['items'])
                if (vacancies['pages'] - page) <= 1:
                    break
                time.sleep(0.2)
        return vacancies_lst


class DBManager:
    connection = None
    cursor = None

    def __init__(self, db_name: str, filename="database.ini", section="postgresql") -> None:
        parser = ConfigParser()
        filepath = os.path.join(os.path.dirname(__file__), filename)
        parser.read(filepath, encoding='utf-8')

        db = {}
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
        try:
            self.create_database(db, db_name)
        except psycopg2.ProgrammingError:
            print(f'Подключаюсь к базе данных {db_name}')

        db.update({'dbname': db_name})

        conn = psycopg2.connect(**db)
        self.connection = conn
        self.cursor = conn.cursor()

    def query(self, string: str, params: tuple):
        """Выполняет запросы к sql на запись"""
        if params:
            self.cursor.execute(string, params)
        else:
            self.cursor.execute(string)

        self.connection.commit()

    def get_companies_and_vacancies_count(self) -> list:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        result = None
        self.cursor.execute("""SELECT company_name, COUNT(*) FROM employers
                            JOIN vacancies USING(employer_id)
                            GROUP BY company_name
                            ORDER BY company_name""")
        if self.cursor.description is not None:
            result = self.cursor.fetchall()

        return result

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию."""
        result = None
        self.cursor.execute("""SELECT employers.company_name, vacancy_title, salary_from, salary_to, 
                            currency, vacancy_url FROM vacancies 
                            JOIN employers using(employer_id)""")
        if self.cursor.description is not None:
            result = self.cursor.fetchall()

        return result

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        # result = None
        # self.cursor.execute('''
        # ''')
        # if self.cursor.description is not None:
        #     result = self.cursor.fetchall()
        #
        # return result

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self, search_query):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        result = None
        self.cursor.execute("""SELECT * FROM vacancies
                            WHERE vacancy_title like '%{}%'""".format(search_query))
        if self.cursor.description is not None:
            result = self.cursor.fetchall()

        return result

    def close_connection(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def close_cursor(self) -> None:
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None

    @staticmethod
    def create_database(params, db_name) -> None:
        """Создает новую базу данных."""
        conn = psycopg2.connect(**params)
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        cur.execute(f"CREATE DATABASE {db_name};")

        cur.close()
        conn.close()


# data_base_name = 'my_new_db'
# psql = DBManager(data_base_name)
#
# psql.close_cursor()
# psql.close_connection()
# print()
