r"""
Написать скрипт, создающий из config.yaml стартер для проекта со следующей структурой:
        |--my_project
           |--settings
           |  |--__init__.py
           |  |--dev.py
           |  |--prod.py
           |--mainapp
           |  |--__init__.py
           |  |--models.py
           |  |--views.py
           |  |--templates
           |     |--mainapp
           |        |--base.html
           |        |--index.html
           |--authapp
           |  |--__init__.py
           |  |--models.py
           |  |--views.py
           |  |--templates
           |     |--authapp
           |        |--base.html
           |        |--index.html
    Предусмотреть возможные исключительные ситуации.
"""
from os import walk, makedirs, stat
from os.path import join, isdir, exists
from pickle import dumps, loads


def read_file(path):
    """Построчное чтение файла генератором"""
    with open(path, encoding='utf-8') as file:  # открываем файл источник
        for string in file:
            yield string.strip()                # и возвращаем из него данные по строке на запрос


def create_config(config_path='', path=''):
    """Считать содержимое папки в файл конфигурации ('куда сохраняем', 'откуда читаем')"""
    pass


def create_starter(config_path, path='', project_name='my_project'):
    """Собрать стартер из файла конфигурации ('откуда читаем', 'где создаем', 'имя проекта')"""
    pass


commands_dict = {'read': create_config, 'create': create_starter}     # словарь функций

# ЗАПРОС ДЕЙСТВИЯ
action = input('Введите необходимую операцию со списком. Для справки ничего не вводите, нажмите Enter\n>>> ')

command, *args = action.split()   # разбиваем запрос на список
if not command or not commands_dict.get(command):  # если команда не распознана выводим справку
    print('HELP\n'
          'read <config_path> <template_folder_path>  - чтение содержимого папки <template_folder_path>\n'
          '                                             в файл <config_path>\n'
          'create <config_path> <path> <project_name> - воссоздание иерархии стартера из файла <config_path>\n'
          '                                             в директории <path> (по умолчанию в папке запуска скрипта)\n'
          '                                             в проект <project_name> (по умолчанию "my_project")'
          )
else:
    commands_dict.get(command)(*args)                    # иначе выполняем функцию из словаря
