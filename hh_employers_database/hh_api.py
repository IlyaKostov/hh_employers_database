import time
from typing import Any

import requests


class HeadHunterAPI:
    EMPLOYER_ID = ['1740', '15478', '2180', '64174', '84585', '1057', '3776', '3529', '78638', '41862']
    URL_VACANCIES = "https://api.hh.ru/vacancies"
    URL_EMPLOYERS = "https://api.hh.ru/employers/{employer_id}"
    MAX_PAGES = 15

    def get_vacancies_by_employers(self) -> list[dict[str, Any]]:
        """
        Получение списка вакансий и данных о работодателях с платформы HeadHunter
        :return: list[dict[str, Any]]
        """
        data = []

        for employer in self.EMPLOYER_ID:
            employer_data = requests.get(self.URL_EMPLOYERS.format(employer_id=employer)).json()

            vacancies_lst = []
            for page in range(self.MAX_PAGES):
                params = {'per_page': 100,
                          'page': page,
                          'order_by': "publication_time",
                          'area': [113, 16, 40],
                          'employer_id': employer
                          }
                vacancies = requests.get(self.URL_VACANCIES, params=params).json()
                vacancies_lst.extend(vacancies['items'])
                if (vacancies['pages'] - page) <= 1:
                    break
                time.sleep(0.05)

            data.append({'employer': employer_data, 'vacancies': vacancies_lst})

        return data
