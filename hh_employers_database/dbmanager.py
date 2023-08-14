import psycopg2


class DBManager:
    connection = None
    cursor = None

    def __init__(self, db_name: str, params: dict) -> None:
        self.create_database(params, db_name)

        params.update({'dbname': db_name})

        conn = psycopg2.connect(**params)
        self.connection = conn
        self.cursor = conn.cursor()

    def query(self, string: str, params: tuple) -> None:
        """Выполняет запросы к sql на запись"""
        if params:
            self.cursor.execute(string, params)
        else:
            self.cursor.execute(string)

    def get_companies_and_vacancies_count(self) -> None:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.cursor.execute("""SELECT employer_name, COUNT(*) FROM employers
                            JOIN vacancies USING(employer_id)
                            GROUP BY employer_name
                            ORDER BY employer_name""")

    def get_all_vacancies(self) -> None:
        """Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию."""
        self.cursor.execute("""SELECT employer_name, vacancy_title, salary_from, salary_to, 
                            currency, vacancy_url FROM vacancies 
                            JOIN employers using(employer_id)""")

    def get_avg_salary(self) -> tuple:
        """Получает среднюю зарплату по вакансиям."""
        result = None
        self.cursor.execute("""SELECT ROUND((AVG(salary_from) + AVG(salary_to)) / 2, 2) AS avg_salary, currency 
                            FROM vacancies
                            WHERE currency = 'RUR'
                            GROUP BY currency""")
        if self.cursor.description is not None:
            result = self.cursor.fetchone()

        return result

    def get_vacancies_with_higher_salary(self) -> None:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        self.cursor.execute("""SELECT employer_name, vacancy_title, city, salary_from, salary_to, 
                            currency, experience, vacancy_url FROM vacancies
                            JOIN employers USING(employer_id)
                            WHERE currency = 'RUR' 
                            AND salary_from > (SELECT ROUND((AVG(salary_from) + AVG(salary_to)) / 2, 2) FROM vacancies) 
                            OR salary_to > (SELECT ROUND((AVG(salary_from) + AVG(salary_to)) / 2, 2) FROM vacancies)""")

    def get_vacancies_with_keyword(self, search_query: str) -> None:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        self.cursor.execute("""SELECT employer_name, vacancy_title, city, requirement, responsibility, 
                            salary_from, salary_to, currency, experience, vacancy_url FROM vacancies
                            JOIN employers USING(employer_id)
                            WHERE vacancy_title like '%{}%'""".format(search_query))

    def close_connection(self) -> None:
        """Закрывает курсор"""
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def close_cursor(self) -> None:
        """Закрывает соединение"""
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None

    @staticmethod
    def create_database(params, db_name) -> None:
        """Создает новую базу данных."""
        conn = psycopg2.connect(**params)
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
        cur.execute(f"CREATE DATABASE {db_name};")

        cur.close()
        conn.close()
