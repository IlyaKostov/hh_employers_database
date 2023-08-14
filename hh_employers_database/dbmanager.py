import os
from configparser import ConfigParser

import psycopg2


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

        self.create_database(db, db_name)

        db.update({'dbname': db_name})

        conn = psycopg2.connect(**db)
        self.connection = conn
        self.cursor = conn.cursor()

    def query(self, string: str, params: tuple) -> None:
        """Выполняет запросы к sql на запись"""
        if params:
            self.cursor.execute(string, params)
        else:
            self.cursor.execute(string)

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

        cur.execute(f"DROP DATABASE  IF EXISTS {db_name};")
        cur.execute(f"CREATE DATABASE {db_name};")

        cur.close()
        conn.close()
