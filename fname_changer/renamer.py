def translit(file: str) -> dict:
    translit_dict = {}
    flow = open(file).read().splitlines()
    for line in flow:
        line = line.split('\t')
        translit_dict[line[0]] = line[1]
    return translit_dict


if __name__ == '__main__':
    b = translit('/home/yolter/Dev/fname_changer/transliteration.txt')
    print(b)
