from pathlib import Path
import taglib


def table_convert(file: str) -> dict:
    """преобразовывает файл с транслитерацией в словарь"""
    with open(file) as flow:
        # удаляем символ переноса строки '\n'
        flow = flow.read().splitlines()
        # создаем словарь транслитерации в нижнем регистре
        translit = {
            ru: en for ru, en in [line.split('\t') for line in flow]
        }
        # создаем словарь транслитерации в верхнем регистре
        up_translit = {
            RU.upper(): translit[RU].upper() for RU in translit
            if RU != 'ь' and RU != 'ъ'
        }
        # объединяем оба словаря
        translit.update(up_translit)
        return translit


def translator_ru_en(content: str, table_ru_en: dict) -> str:
    """кириллические символы заменяет латинскими из таблицы транслитерации,
     непереводимые символы (ь, ъ) удаляет, символ "_" заменяет на пробел"""
    content = list(content)
    for letter in content:
        if letter in table_ru_en:
            if letter == 'ь' or letter == 'ъ':
                content[content.index(letter)] = ''
            else:
                content[content.index(letter)] = table_ru_en[letter]
        elif letter == '_':
            content[content.index(letter)] = ' '
    content = ''.join(content)
    return content


def renamer(folder: str, translit_table: dict) -> None:
    """если имя файла или теги содержат кириллические символы,
     заменяет их латинской транслитерацией
     атрибут folder ожидает абсолютный путь каталога, содержащий файлы
    с расширением .mp3"""
    # проверяем существование указанного пути
    if Path(folder).exists():
        # получаем путь каждого файла
        for link in Path(folder).glob('**/*.mp3'):
            # переименовываем русское название файла в транслит
            file_name = translator_ru_en(Path(link).stem, translit_table)
            new_link = f'{Path(link).parent}/{file_name}{Path(link).suffix}'
            link.rename(new_link)
            # переименовываем руксские теги файла в транслит
            song = taglib.File(new_link)
            for tag in song.tags:
                song.tags[tag] = [translator_ru_en(''.join(song.tags[tag]),
                                                   translit_table)]
            song.save()
            song.close()


if __name__ == '__main__':
    transliter = table_convert(
        '/transliteration_ru_en.txt')
    # print(transliter)
    renamer('/home/yolter/Downloads/тест', transliter)
