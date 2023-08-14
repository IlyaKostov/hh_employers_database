import os

import psycopg2
from prettytable import PrettyTable

my_table = PrettyTable()


def filling_database(psql, data) -> None:
    for employers in data:
        employer_data = employers['employer']
        psql.query("""INSERT INTO employers(employer_name, employer_site_url, employer_hh_url) 
                         VALUES (%s, %s, %s)
                         RETURNING employer_id""",
                   (employer_data['name'], employer_data['site_url'], employer_data['alternate_url']))
        employer_id = psql.cursor.fetchone()[0]

        employer_vacancies = employers['vacancies']
        for vacancy in employer_vacancies:
            salary = vacancy.get('salary')
            if salary is not None:
                salary_from = salary['from']
                salary_to = salary['to']
                currency = salary['currency']
            else:
                salary_from = salary
                salary_to = salary
                currency = salary

            psql.query("""INSERT INTO vacancies(vacancy_title, employer_id, city, salary_from, salary_to, currency, 
                        published_date, requirement, responsibility, experience, vacancy_url) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                       (vacancy['name'], employer_id, vacancy['area']['name'], salary_from, salary_to, currency,
                        vacancy['published_at'], vacancy['snippet']['requirement'],
                        vacancy['snippet']['responsibility'], vacancy['experience']['name'], vacancy['alternate_url']))

    psql.close_cursor()
    psql.connection.commit()


def execute_sql_script(cur, filename: str) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        script = file.read()
        cur.execute(script)


def result_conversion(result: list[tuple | list], column_name: list[str]) -> str:
    my_table.field_names = column_name
    my_table.add_rows(result)
    return my_table.get_string()


def drop_database(params: dict, db_name: str) -> None:
    """Создает новую базу данных."""
    conn = psycopg2.connect(**params)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    cur.execute("""SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = %s
                AND pid <> pg_backend_pid();""", (db_name,))
    cur.execute(f"DROP DATABASE IF EXISTS {db_name};")

    cur.close()
    conn.close()
