import os
import requests
from abc import ABC, abstractmethod


class ParsingError(Exception):
    """Пользовательский класс ошибок"""

    def __str__(self):
        """Возвращает текст ошибки"""
        return 'Ошибка получения данных'


class abc_api(ABC):
    """Абстрактный класс для работы с работы API"""

    @abstractmethod
    def get_vacancies(self):
        """Получает вакансии head hunter и superjob"""
        pass

    @abstractmethod
    def get_request(self):
        """Получение ответа на запрос от API сервиса по вакансиям"""
        pass

    @abstractmethod
    def format_vacancies(self):
        """Возвращает вакансии в едином формате"""
        pass


class HeadHunter(abc_api):
    def __init__(self, keyword):
        """Класс для API hh.ru"""
        self.__header = {'User-Agent': "unknown"}
        self.__params = {
            'text': keyword,
            'page': 0,
            'per_page': 10

            ,
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary):
        pay_salary = [None, None]
        if salary and salary['from'] and salary['from'] != 0:
            if salary['currency'].lower() == 'rub':
                pay_salary[0] = salary['from']
                if salary and salary['payment_to'] and salary['payment_to'] != 0:
                    if salary['currency'].lower() == 'rub':
                        pay_salary[1] = salary['payment_to']
        return pay_salary

    def get_request(self):
        response = requests.get('https://api.hh.ru/vacancies',
                                headers=self.__header,
                                params=self.__params
                                )
        if response.status_code != 200:
            raise ParsingError
        return response.json()['items']

    def get_vacancies(self, page_count=1):
        """Получает вакансии head hunter"""
        while self.__params['page'] < page_count:
            print(f"Получаем сведения hh, страница{self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except  ParsingError:
                print('Ошибка получения данных!')
                break
            print(f"Найдено ({len(values)}) вакансий \n")
            self.__vacancies.extend(values)
            self.__params['page'] += 1

    def format_vacancies(self):
        vacancies = []
        if self.__vacancies:
            for row in self.__vacancies:
                salary_from, salary_to = self.get_salary(row['salary'])
                temp_dict = {
                    'title': row['name'],
                    'salary_from': salary_from,
                    'salary_to': salary_to,
                    'discription': row['snippet']['responsibility'],
                    'company_name': row['employer']['name'],
                    'link': row['alternate_url']
                }
                vacancies.append(temp_dict)
        return vacancies


class SuperJob(abc_api):
    """Класса для superjob"""

    def __init__(self, keyword):
        self.__header = {
            "X-Api-App-Id": os.getenv('SJ_API_KEY')
        }
        self.__params = {
            "keyword": keyword,
            "page": 0,
            "count": 10
        }
        self.__vacancies = []

    def get_request(self):
        response = requests.get('https://api.superjob.ru/2.0/vacancies',
                                headers=self.__header,
                                params=self.__params
                                )
        if response.status_code != 200:
            raise ParsingError
        return response.json()['objects']

    def get_vacancies(self, page_count=1):
        """Получает вакансии Superjob"""
        while self.__params['page'] < page_count:
            print(f"Получаем сведения superjob, страница{self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка получения данных!')
                break
            print(f"Найдено ({len(values)}) вакансий \n")
            self.__vacancies.extend(values)
            self.__params['page'] += 1

    @staticmethod
    def get_salary(data):
        pay_salary = [None, None]
        if data and data['payment_from'] and data['payment_from'] != 0:
            if data['currency'].lower() == 'rub':
                pay_salary[0] = data['payment_from']
                if data and data['payment_to'] and data['payment_to'] != 0:
                    if data['currency'].lower() == 'rub':
                        pay_salary[1] = data['payment_to']
        return pay_salary

    def format_vacancies(self):
        vacancies = []
        if self.__vacancies:
            for row in self.__vacancies:
                salary_from, salary_to = self.get_salary(row)
                temp_dict = {
                    'title': row['profession'],
                    'salary_from': salary_from,
                    'salary_to': salary_to,
                    'discription': row['vacancyRichText'],
                    'company_name': row['firm_name'],
                    'link': row['link']
                }
                vacancies.append(temp_dict)
        return vacancies
