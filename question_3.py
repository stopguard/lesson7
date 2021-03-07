r"""
Написать скрипт, который собирает все шаблоны стартера из задания 2 в одну папку templates.
    исходные файлы необходимо оставить
"""
from os import walk, makedirs, getcwd
from os.path import join, relpath, getsize, exists
from os.path import split as path_split
from shutil import copy2

# выявляем системный разделитель путей для мультиплатформенности(надеюсь из под линуха сработает)
home_path = getcwd()                                              # забираем текущий путь
splited_path = path_split(home_path)                              # разбиваем его на последний элемент и путь
dir_sep = home_path[len(splited_path[0]):-len(splited_path[1])]   # выкидываем последний элемент и путь к нему из строки


class SizeError(Exception):
    """Ошибка объёма данных"""
    pass


def read_starter(path):
    """Создать список шаблонов в указанном стартере"""
    # проверяем объём папок
    starter_size = 0    # обнуляем размер шаблонов
    paths_score = 0              # количество папок
    files_score = 0              # количество файлов
    for f_path, _, f_names in walk(path):       # первый проход валком - для подсчёта объёма данных
        if 'templates' in relpath(f_path, path):    # если в относительном пути присутствует templates
            paths_score += 1                            # инкремент счётчика папок
            for f_name in f_names:                      # проход по имеющимся в папке файлам
                files_score += 1                                # инкремент счётчика файлов
                starter_size += getsize(join(f_path, f_name))   # инкремент объёма текущего файла к размеру стартера
                if starter_size > 100 * 1024 ** 2:              # если объём больше 100МБ завершаем скрипт ошибкой
                    raise SizeError                                 # лежит в цикле чтобы не продолжать когда всё ясно
    print(f'  Объём данных: {starter_size} байт\n'
          f' Найдено папок: {paths_score},\n'
          f'        файлов: {files_score}.\n'
          f'Приступаю к чтению стартера...')     # выводим результаты подсчёта
    # результатом преобразования стартера является:
    # кортеж из 2 списков:
    #   - список путей для создания структуры
    #   - список путей к файлам
    config = ([], [])   # объявляем заготовку конфига
    _fold_path = []     # временная переменная для разбитого на части пути
    for paths, folders, names in walk(path):        # второй проход валком, для формирования списка необходимого
        if 'templates' in relpath(paths, path):         # если в относительном пути присутствует templates
            _fold_path = relpath(paths, path).split(dir_sep)  # получаем относительный путь, разбиваем его на список
            if not folders:                                 # если в пути нет вложенных папок
                config[0].append(_fold_path)                   # добавляем его в список путей
            for name in names:                              # проход по списку файлов в текущей папке
                _file_path = _fold_path[:]                     # копируем список текущего относительного пути
                _file_path.append(name)                        # добавляем в него имя файла
                config[1].append(_file_path[:])                # добавляем в список файлов путь к файлу и его содержимое
    # print(*config[0], sep='\n')   # вывод списка папок
    # print(*config[1], sep='\n')   # вывод списка путей к файлам
    return config  # возвращаем результат работы


def copy_templates(path):
    """Собрать стартер из файла конфигурации ('откуда читаем', 'где создаем', 'имя проекта')"""
    if not exists(path):                                # если целевой папки не существует
        raise FileNotFoundError(f'{path} not found')        # поднимаем ошибку
    folders, files = read_starter(path)                 # собираем список папок и файлов из прочитанного в стартере
    for folder in folders:                              # проходим по списку папок
        folder = join(path, *folder[folder.index('templates'):])  # собираем путь в кучу отбросив всё что до 'template'
        makedirs(folder)                                    # создаём путь
    print('Иерархия создана')                           # отчёт о готовности структуры папок
    for file in files:                                  # проходим по списку файлов
        file_path = join(path, *file)                               # собираем в кучу путь к файлу исходнику
        templ_path = join(path, *file[file.index('templates'):])    # собираем в кучу целевой путь
        copy2(file_path, templ_path)                                # копируем файл из исходного пути в целевой
    print('Файлы созданы')                              # отчёт о готовности файлов
    return 'Шаблоны успешно скопированы'                # возвращаем результат работы


"""ИСПОЛНЯЕМАЯ ЧАСТЬ"""
# запрос адреса стартера:
starter_path = input('\nВведите путь к стартеру для сбора шаблонов.\n>>> ')
try:
    print(copy_templates(starter_path))                     # если всё в порядке - выводим отчёт функции
except FileExistsError as error:                        # если происходит попытка перезаписи файла/папки
    print(f'Вы использовали существующий путь: {error}')    # выводим содержимое ошибки
except FileNotFoundError as error:                      # если происходит попытка прочитать несуществующий конфиг
    print(f'Указанного пути не существует: {error}')        # выводим содержимое ошибки
except SizeError:                                       # если попытка прочитать слишком объёмные данные
    print("Ошибка - объём данных больше 100 МБ")            # выводим содержимое ошибки
except Exception as error:                              # для остальных ошибок
    print(f"Неизвестная ошибка: {error}")                   # выводим содержимое ошибки
