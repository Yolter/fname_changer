from pathlib import Path


def translit(file: str) -> dict:
    """преобразовывает файл с транслитерацией в словарь"""
    translit_dict = {}
    with open(file) as flow:
        flow = flow.read().splitlines()
        for line in flow:
            line = line.split('\t')
            translit_dict[line[0]] = line[1]
        return translit_dict


def renamer(folder: str, translit_dict: dict) -> None:
    """если имя файла содержит русские буквы, заменяет их транслитерацией"""
    if Path(folder).exists():  # проверяем существование указанного пути
        for link in Path(folder).glob('**/*.mp3'):  # получаем путь каждого файла
            file_name = list(Path(link).stem)
            for letter in file_name:
                if letter in translit_dict:
                    file_name[file_name.index(letter)] = translit_dict[letter]
            file_name = ''.join(file_name)
            new_link = f'{Path(link).parent}/{file_name}{Path(link).suffix}'
            link.rename(new_link)


if __name__ == '__main__':
    dic = translit('/home/yolter/Dev/fname_changer/transliteration_ru_en.txt')
    renamer('/home/yolter/Downloads/тест', dic)
