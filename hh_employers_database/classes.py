import time

import requests


class HeadHunterAPI:

    EMPLOYER_ID = ['1740', '15478', '2180', '64174', '84585', '1057', '3776', '3529', '78638', '41862']

    # URL = f"https://api.hh.ru/employers/6131/vacancies/active"
    # URL = "https://api.hh.ru/vacancies"
    URL = "https://api.hh.ru/employers/{employer_id}"
    MAX_PAGES = 10

    def get_vacancies(self):
        employers = []
        for employer in self.EMPLOYER_ID:

            employer_data = requests.get(self.URL.format(employer_id=employer)).json()
            employers.append(employer_data)

            time.sleep(0.5)
        return employers

    def get_vacancies(self):
        """
        Получение списка вакансий с платформы HeadHunter
        :param query: текст запроса
        :return: list
        """
        # vacancies_lst = []
        # for page in range(self.MAX_PAGES):
        # params = {'per_page': 100,
        #           'order_by': "publication_time",
        #           'area': [113, 16, 40],
        #           'employer_id': ['6131', '1740', '15478']
        #           } , params=params
        vacancies_lst = []
        for page in range(self.MAX_PAGES):
            params = {'per_page': 100,
                      'page': page,
                      'order_by': "publication_time",
                      'area': [113, 16, 40],

                      }
            vacancies = requests.get(self.URL, params=params).json()
            vacancies_lst.extend(vacancies['items'])
            if (vacancies['pages'] - page) <= 1:
                break
            time.sleep(0.5)
        return vacancies_lst


class DBManager:

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        pass

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию."""
        pass

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        pass
