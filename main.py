from job import HeadHunter, SuperJob
from json_saver import JSONSaver


def main():
    """Основная функция взаимодействия с пользователем"""
    print('Приветствую!\nДанная программа собирает с сайтов HeadHunter и SuperJob 200 вакансий (по 100 с каждого)\n'
          'по ключевому слову и формирует список вакансий.\n')
    keyword = input('Введите название вакансии --->')

    hh_api = HeadHunter(keyword)
    superjob_api = SuperJob(keyword)
    for recruiter in hh_api, superjob_api:
        recruiter.get_vacancies(page_count=10)
        vacancies = recruiter.format_vacancies()
        json_saver = JSONSaver(keyword)
        json_saver.add_vacancies(vacancies)
    # Цикл работы с пользовательскими командами
    while True:
        # Вывод пользовательского меню
        command = input(f"""\nВведите номер команды:
1: Отсортировать вакансии по убыванию максимальной зарплаты и вывести их на экран
2: Вывести на экран топ  N вакансий
3: Вывести на экран вакансии с зарплатой в диапазоне
exit: Выйти из программы\n""")
        # Запуск команды 1:Сортировка вакансий
        if command == '1':
            data = json_saver.sorted_vacancies()
            for v in data:
                print(v)
        # Запуск команды 2: Вывод на экран заданного количества топ вакансий пользователем
        elif command == '2':
            number_vacancies = input('Введите количество входящих в ТОП вакансий --->')
            data = json_saver.sorted_vacancies()
            for r in json_saver.get_top_vacancies(data, int(number_vacancies)):
                print(r)
        # Запуск команды 3: Вывод на экран вакансий с зарплатами в заданном диапазоне пользователем
        elif command == '3':
            range = input('Введите диапазон зарплат через дефис, например 50000-80000 --->')
            for v in json_saver.vacancies_by_salary_range(range):
                print(v)
        elif command.lower() == 'exit':
            break
        else:
            print('Неверная команда')


if __name__ == '__main__':
    main()
