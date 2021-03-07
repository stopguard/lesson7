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
from os.path import join, relpath, getsize
from os.path import split as path_split
from pickle import dump, dumps, load, loads

# выявляем системный разделитель путей для мультиплатформенности(надеюсь из под линуха сработает)
home_path = getcwd()                                              # забираем текущий путь
splited_path = path_split(home_path)                              # разбиваем его на последний элемент и путь
dir_sep = home_path[len(splited_path[0]):-len(splited_path[1])]   # выкидываем последний элемент и путь к нему из строки


def serialise(path):
    """Сериализация содержимого файла в строку байт"""
    with open(path, encoding='utf-8') as file:  # открываем файл источник
        return dumps(file.read())                   # возвращаем сериализованное содержимое


def create_config(config_path='default_config.yaml', path='default_config'):
    """Считать содержимое папки в файл конфигурации ('куда сохраняем', 'откуда читаем')"""
    # проверяем объём папки
    starter_size = 0    # обнуляем размер стартера
    paths_score = 0              # количество папок
    files_score = 0              # количество файлов
    for f_path, _, f_names in walk(path):       # первый проход валком - для подсчёта объёма данных
        paths_score += 1                            # инкремент счётчика папок
        for f_name in f_names:                      # проход по имеющимся в папке файлам
            files_score += 1                                # инкремент счётчика файлов
            starter_size += getsize(join(f_path, f_name))   # инкремент объёма текущего файла к размеру стартера
            # если объём больше 100МБ завершаем скрипт
            if starter_size > 100 * 1024 ** 2:
                return "Ошибка - объём данных больше 100 МБ"  # лежит в цикле чтобы не продолжать когда и так всё ясно
    print(f'  Объём данных: {starter_size} байт\n'
          f' Найдено папок: {paths_score},\n'
          f'        файлов: {files_score}.\n'
          f'Приступаю к чтению стартера в файл...')     # выводим результаты подсчёта
    # результатом сериализации стартера является:
    # список из 2 списков:
    #   - список путей для создания структуры
    #   - список из списков:
    #       - путь
    #       - и его сериализованное содержимое
    config = [[], []]   # объявляем заготовку конфига
    _fold_path = []     # временная переменная для разбитого на части пути
    for paths, folders, names in walk(path):            # второй проход валком, для формирования конфига
        _fold_path = relpath(paths, path).split(dir_sep)    # получаем относительный путь, разбиваем его на список
        if not folders:                                     # если в пути нет вложенных папок
            config[0].append(_fold_path)                        # добавляем его в список путей
        for name in names:                                  # проход по списку файлов в текущей папке
            f_str = serialise(join(paths, name))               # сериализуем содержимое файла
            _file_path = _fold_path[:]                         # копируем список текущего относительного пути
            _file_path.append(name)                            # добавляем в него имя файла
            config[1].append([_file_path[:], f_str])           # добавляем в список файлов путь к файлу и его содержимое
    if not config_path.endswith('.yaml'):               # если в указанном пути к создаваемому конфигу нет расширения
        config_path += '.yaml'                              # добавляем его
    with open(config_path, 'xb') as f:                  # открываем файл конфига без перезаписи
        dump(config, f)                                     # сериализуем в него полученный список
    return "Сохранение конфигурации выполнено успешно"  # возвращаем результат работы


def create_starter(config_path='default_config.yaml', path='', project_name='my_project'):
    """Собрать стартер из файла конфигурации ('откуда читаем', 'где создаем', 'имя проекта')"""
    if not config_path.endswith('.yaml'):               # проверяем указано ли расширение в файле конфига
        config_path += '.yaml'                              # если нет, добавляем его
    with open(config_path, 'rb') as f:                  # открываем конфиг
        config = load(f)                                    # десериализуем его
    folders = config[0]                                 # забираем из полученного список папок
    files = config[1]                                   # и список с файлами и их содержимым
    for folder in folders:                              # проходим по списку папок
        folder = join(path, project_name, *folder)          # собираем путь в кучу
        makedirs(folder)                                    # создаём путь
    print('Иерархия создана')                           # отчёт о готовности структуры папок
    for file in files:                                  # проходим по списку файлов
        file_path = join(path, project_name, *file[0])      # собираем путь к файлу в кучу
        with open(file_path, 'x', encoding='utf-8') as f:   # т.к. все папки уже созданы можно сразу открывать на запись
            f.write(loads(file[1]))                             # десериализуем второй элемент списка в файл
    print('Файлы созданы')                              # отчёт о готовности файлов
    return 'Стартер успешно загружен'                   # возвращаем результат работы


"""ИСПОЛНЯЕМАЯ ЧАСТЬ"""
commands_dict = {'read': create_config, 'create': create_starter}     # словарь функций

while True:  # цикл не остановится пока пользователь не отправит пустую строку
    # запрос действия:
    action = input('\nВведите необходимую операцию со стартером. Для выхода ничего не вводите, нажмите Enter\n'
                   'Для справки введите help\n>>> ')
    try:
        command, *args = action.split()             # разбиваем запрос на список
        print(commands_dict.get(command)(*args))    # выполняем функцию из словаря с выводом отчёта
    except ValueError as error:                 # если ничего не введено
        print('Выход из программы')
        break                                       # выходим из цикла
    except TypeError as error:                  # если введён непредусмотренный аргумент выводим справку
        print('HELP\n'
              'read <config_path> <template_folder_path>  - чтение содержимого папки <template_folder_path>\n'
              '                                             в файл <config_path>\n'
              'create <config_path> <path> <project_name> - воссоздание иерархии стартера из файла <config_path>\n'
              '                                             в директории <path> (по умолчанию в папке запуска)\n'
              '                                             в проект <project_name> (по умолчанию "my_project")'
              )
    except FileExistsError as error:                        # если происходит попытка перезаписи файла/папки
        print(f'Вы использовали существующий путь: {error}')    # выводим содержимое ошибки
    except FileNotFoundError as error:                      # если происходит попытка прочитать несуществующий конфиг
        print(f'Указанного пути не существует: {error}')        # выводим содержимое ошибки
    except Exception as error:                              # для остальных ошибок
        print(f"Неизвестная ошибка: {error}")                   # выводим содержимое ошибки
