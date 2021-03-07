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
from os import walk, makedirs, getcwd
from os.path import join, exists, relpath, getsize
import os.path
from pickle import dump, dumps, load, loads

home_path = getcwd()
splited_path = os.path.split(home_path)
dir_sep = home_path[len(splited_path[0]):-len(splited_path[1])]


def read_file(path):
    """Построчное чтение файла генератором"""
    with open(path, encoding='utf-8') as file:  # открываем файл источник
        for string in file:
            yield string.strip()                # и возвращаем из него данные по строке на запрос


def serialise(path):
    """Сериализация содержимого файла в строку байт"""
    with open(path, encoding='utf-8') as file:  # открываем файл источник
        return dumps(file.read())


def create_config(config_path='default_config.yaml', path='default_config'):
    """Считать содержимое папки в файл конфигурации ('куда сохраняем', 'откуда читаем')"""
    # проверить объём папки
    starter_size = 0
    paths_score = 0
    files_score = 0
    for f_path, _, f_names in walk(path):
        paths_score += 1
        for f_name in f_names:
            files_score += 1
            starter_size += getsize(join(f_path, f_name))
            # если объём больше 100МБ завершаем скрипт
            if starter_size > 100 * 1024 ** 2:
                return "Ошибка - объём данных больше 100 МБ"  # лежит в цикле чтобы не продолжать когда и так всё ясно
    print(f'  Объём данных: {starter_size} байт\n'
          f' Найдено папок: {paths_score},\n'
          f'        файлов: {files_score}.\n'
          f'Приступаю к чтению стартера в файл...')
    # список из 2 списков
    #   - список путей для создания структуры
    #   - список из списков
    #       - пути
    #       - и его сериализованного содержимого
    config = [[], []]
    _fold_path = []
    for paths, folders, names in walk(path):
        _fold_path = relpath(paths, path).split(dir_sep)
        if not folders:
            config[0].append(_fold_path)
        for name in names:
            _file_path = _fold_path[:]
            f_str = serialise(join(paths, name))
            _file_path.append(name)
            config[1].append([_file_path[:], f_str])
    if not config_path.endswith('.yaml'):
        config_path += '.yaml'
    with open(config_path, 'xb') as f:
        dump(config, f)
    return "Сохранение конфигурации выполнено успешно"


def create_starter(config_path='default_config.yaml', path='', project_name='my_project'):
    """Собрать стартер из файла конфигурации ('откуда читаем', 'где создаем', 'имя проекта')"""
    if not config_path.endswith('.yaml'):
        config_path += '.yaml'
    with open(config_path, 'rb') as f:
        config = load(f)
    folders = config[0]
    files = config[1]
    for folder in folders:
        folder = join(path, project_name, *folder)
        makedirs(folder)
    print('Иерархия создана')
    for file in files:
        file_path = join(path, project_name, *file[0])
        with open(file_path, 'x', encoding='utf-8') as f:
            f.write(loads(file[1]))
    print('Файлы созданы')
    return 'Стартер успешно загружен'


commands_dict = {'read': create_config, 'create': create_starter}     # словарь функций

# ЗАПРОС ДЕЙСТВИЯ
action = input('Введите необходимую операцию со стартером. Для справки ничего не вводите, нажмите Enter\n>>> ')

try:
    command, *args = action.split()  # разбиваем запрос на список
    print(commands_dict.get(command)(*args))                    # иначе выполняем функцию из словаря
except (TypeError, ValueError):
    print('HELP\n'
          'read <config_path> <template_folder_path>  - чтение содержимого папки <template_folder_path>\n'
          '                                             в файл <config_path>\n'
          'create <config_path> <path> <project_name> - воссоздание иерархии стартера из файла <config_path>\n'
          '                                             в директории <path> (по умолчанию в папке запуска скрипта)\n'
          '                                             в проект <project_name> (по умолчанию "my_project")'
          )
except FileExistsError:
    print('Вы использовали существующий путь')
except Exception as error:
    print(f"Неизвестная ошибка: {error}")
