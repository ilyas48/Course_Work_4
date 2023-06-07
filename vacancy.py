class Vacancy:
    """Класс с вакансиями"""
    __slots__ = ('__title', '__salary_from', '__salary_to', '__discription', '__company_name', '__link')

    def __init__(self, title, salary_from, salary_to, description, company_name, link):
        """Инициализация класса вакансий"""
        self.__title = title
        self.__salary_from = salary_from
        self.__salary_to = salary_to
        self.__discription = description
        self.__company_name = company_name
        self.__link = link

    def __str__(self):
        """Выводит информацию о вакансии для пользователя"""
        salary_min = f" ОТ {self.__salary_from}" if self.__salary_from else ""
        salary_max = f"ДО {self.__salary_to}" if self.__salary_to else ""
        if self.__salary_from is None and self.__salary_to is None:
            salary_max = "Зарплата не указана"
        return f"""Вакансия: {self.__title} в компанию {self.__company_name},\
 зарплата {salary_min} {salary_max}
 ссылка на вакансию {self.__link}\n"""

    @property
    def salary_from(self):
        """Возвращает зарплату От"""
        return self.__salary_from

    @property
    def salary_to(self):
        """Возвращает зарплату До"""
        return self.__salary_to

    def __lt__(self, other):
        """Метод сравнения вакансий"""
        if not self.salary_from and not self.salary_to:
            return True
        elif not self.salary_from:
            if not other.salary_from and not other.salary_to:
                return False
            elif not other.salary_to:
                return self.salary_to <= other.salary_from
            elif not other.salary_from:
                return self.salary_to <= other.salary_to
            else:
                if self.salary_to > other.salary_from:
                    return self.salary_to < other.salary_to
        elif self.salary_from and not self.salary_to:
            if not other.salary_from and not other.salary_to:
                return False
            elif not other.salary_to:
                return self.salary_from <= other.salary_from
            elif not other.salary_from:
                return self.salary_from < other.salary_to
            else:
                return (self.salary_from <= other.salary_from) and (self.salary_from < other.salary_to)
        else:
            if not other.salary_from and not other.salary_to:
                return False
            elif not other.salary_to:
                return (self.salary_from <= other.salary_from) and (self.salary_to <= other.salary_from)
            elif not other.salary_from:
                return (self.salary_from <= other.salary_to) and (self.salary_to <= other.salary_to)
            else:
                return (self.salary_from <= other.salary_from) and (self.salary_to < other.salary_to)
