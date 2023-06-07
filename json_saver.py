from abc import ABC, abstractmethod
import json
from vacancy import Vacancy


class FileSaver(ABC):
    """Абстрактный класс для сохранения в файлы"""

    @abstractmethod
    def add_vacancies(self, information):
        """Добавляет вакансию"""
        pass


class JSONSaver(FileSaver):
    """Класс для сохранения файла"""

    def __init__(self, keyword):
        """Конструктор класса JSONSaver"""
        self.__filename = f'{keyword.title()}.json'

    @property
    def filename(self):
        """Возвращает имя файла"""
        return self.__filename

    def add_vacancies(self, information):
        """Добавляет вакансию в файл"""
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(information, file, indent=4, ensure_ascii=False)

    def select(self):
        """Чтение вакансий из файла"""
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            vacancies = []
            for d_dict in data:
                v = Vacancy(d_dict['title'], d_dict['salary_from'], d_dict['salary_to'], d_dict['discription'],
                            d_dict['company_name'], d_dict['link'])
                vacancies.append(v)
        return vacancies

    def sorted_vacancies(self):
        """Производит сортировку данных их файла
         с вакансиями по возрастанию зарплат"""
        vacancies = self.select()
        vacancies = sorted(vacancies)
        return vacancies

    def get_top_vacancies(self, data, num_top=1):
        """Возвращает указанное количество топ
        вакансий"""
        print(f"\n Топ {num_top} вакансий\n")
        vacancies = [data[-i] for i in range(1, num_top + 1)]
        return vacancies

    def vacancies_by_salary_range(self, salary_range):
        """Выводит зарплаты в заданном диапазоне"""
        data = self.select()
        if isinstance(salary_range, str) and '-' in salary_range:
            salary_min_str, salary_max_str = salary_range.split('-')
            salary_min = int(salary_min_str)
            salary_max = int(salary_max_str)
        else:
            print("Неверный формат диапазона")

        if salary_min > salary_max:
            t = salary_max
            salary_max = salary_min
            salary_min = t
        elif salary_min == salary_max:
            print("Не указан диапазон")

        vacancies = []

        for vacancy in data:
            salary_from = vacancy.salary_from if vacancy.salary_from else 0
            salary_to = vacancy.salary_to if vacancy.salary_to else 0
            if salary_min <= salary_from < salary_max or salary_min < salary_to <= salary_max:
                vacancies.append(vacancy)

        return vacancies
