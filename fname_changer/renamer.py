from pathlib import Path
import taglib


def translit(file: str) -> dict:
    """преобразовывает файл с транслитерацией в словарь"""
    with open(file) as flow:
        # удаляем символ переноса строки '\n'
        flow = flow.read().splitlines()
        # создаем словарь транслитерации в нижнем регистре
        translit_dict = {
            ru: en for ru, en in [line.split('\t') for line in flow]
        }
        # создаем словарь транслитерации в верхнем регистре
        up_translit_dict = {
            RU.upper(): translit_dict[RU].upper() for RU in translit_dict
            if RU != 'ь' and RU != 'ъ'
        }
        # объединяем оба словаря
        translit_dict.update(up_translit_dict)
        return translit_dict


def renamer(folder: str, translit_table: dict) -> None:
    """если имя файла содержит русские буквы, заменяет их транслитерацией"""
    # проверяем существование указанного пути
    if Path(folder).exists():
        # получаем путь каждого файла
        for link in Path(folder).glob('**/*.mp3'):
            # переименовываем русское название файла в транслит
            file_name = list(Path(link).stem)
            for letter in file_name:
                if letter in translit_table:
                    file_name[file_name.index(letter)] = translit_table[letter]
                    if letter == 'ь' or letter == 'ъ':
                        file_name[file_name.index(letter)] = ''
                elif letter == '_':
                    file_name[file_name.index(letter)] = ' '
            file_name = ''.join(file_name)
            new_link = f'{Path(link).parent}/{file_name}{Path(link).suffix}'
            link.rename(new_link)
            # переименовываем руксские теги файла в транслит
            song = taglib.File(link)
            for tag in song.tags.values():
                tag = list(''.join(tag))
                for letters in tag:
                    if letters in translit_table:
                        tag[tag.index(letters)] = translit_table[letters]
                        if letters == 'ь' or letters == 'ъ':
                            tag[tag.index(letters)] = ''
                    elif letters == '_':
                        tag[tag.index(letters)] = ' '
                tag = ''.join(tag)

# вывести кусок кода с переинованием в отдельную функцию и закончить с тегами,
# остановился на изменении тега внутри цикла после его переименования








if __name__ == '__main__':
    translit_dict = translit('/home/yolter/Dev/fname_changer/transliteration_ru_en.txt')
    print(translit_dict)
    renamer('/home/yolter/Downloads/тест', translit_dict)
