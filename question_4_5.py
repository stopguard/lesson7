r"""
Написать скрипт, который выводит статистику для заданной папки в виде словаря:
    ключи — верхняя граница размера файла, а значения — кортежи вида (<files_quantity>, [<files_extensions_list>])
    Сохраните результаты в файл <folder_name>_summary.json в той же папке, где запустили скрипт.
"""
from os import walk, getcwd
from os.path import join, abspath, getsize, isdir, exists
from os.path import split as path_split
from json import dump


# выявляем системный разделитель путей для мультиплатформенности(надеюсь из под линуха сработает)
home_path = getcwd()                                              # забираем текущий путь
splited_path = path_split(home_path)                              # разбиваем его на последний элемент и путь
dir_sep = home_path[len(splited_path[0]):-len(splited_path[1])]   # выкидываем последний элемент и путь к нему из строки


def read_summary(folder_path):
    """Сканирует указанную папку"""
    if not exists(folder_path) or not isdir(folder_path):           # если целевой папки не существует
        raise FileNotFoundError(f'Folder {folder_path} not found')      # поднимаем ошибку
    result = {}                                                     # стартуем словарь результатов
    for path, _, files in walk(folder_path):                            # прогулка по подпапкам запрошенной папки
        for file in files:                                                  # прогулка по файлам подпапки
            file_size_to = int('1' + '0' * len(str(getsize(join(path, file)))))   # считаем количество нулей для ключа
            file_type = file.split('.')[-1]                                       # считываем расширение
            # если расширения нет в списке ключа, заодно формируем ключ если его нет
            if not (file_type in result.setdefault(file_size_to, ([0], []))[1]):
                result[file_size_to][1].append(file_type)                           # добавляем расширение в список
            result[file_size_to][0][0] += 1                                     # увеличиваем счётчик ключа
    for key, res in result.items():         # проходим по словарю
        result[key] = (*res[0], res[1])         # разворачиваем в нем списки со счётчиками для выполнения условия задачи
    with open(path_split(abspath(folder_path))[1] + '_summary.json', 'w') as f:  # открываем целевой файл
        dump(result, f, ensure_ascii=False)                                          # сбрасываем в него дамп результата
    return result                                                                # возвращаем результат на вывод


"""ИСПОЛНЯЕМАЯ ЧАСТЬ"""
try:
    paths = input('Укажите папку, которую хотите сканировать:\n>>> ')   # запрос пути к папке
    summary = read_summary(paths)                                       # построение словаря
    sorted_keys = sorted(summary)                                       # сортировка ключей словаря в список
    shift = len(str(sorted_keys[-1]))                                   # получение длины максимального ключа
    print('{')
    for keys in sorted_keys:                                             # проход по сортированным ключам
        print(f'{keys:>{shift}}KB: {summary[keys]}')                            # вывод строки с выравниванием ключа
    print('}')
except FileNotFoundError as error:                  # если происходит попытка прочитать несуществующую папку
    print(f'Указанного пути не существует: {error}')    # выводим содержимое ошибки
except Exception as error:                          # для остальных ошибок
    print(f"Неизвестная ошибка: {error}")               # выводим содержимое ошибки
