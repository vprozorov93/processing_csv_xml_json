import collections
import os
import json
import xml.etree.ElementTree as ETS
import csv


def processing_word_list(word_list):
    top_word_in_dict = {}

    for word in set(word_list):
        if top_word_in_dict.get(word_list.count(word)) is not None:
            top_word_in_dict[word_list.count(word)].append(word)
        else:
            top_word_in_dict[word_list.count(word)] = [word]

    key_list = sorted(list(top_word_in_dict.keys()))
    key_list.reverse()
    top_word_in_list = []

    for key in key_list:
        for item in top_word_in_dict[key]:
            if len(top_word_in_list) < 10:
                top_word_in_list.append(f'"{item}" повторяется {key} раз')
            else:
                break

    print(f'Топ 10 слов в заголовках статей: {top_word_in_list}')


def processing_json(path):
    word_list = []
    with open(path) as file:
        data = json.load(file)

    news_list = data['rss']['channel']['items']
    for news in news_list:
        word_in_title = [word for word in news['title'].lower().split(' ') if len(word) > 6]
        word_list.extend(word_in_title)
        counter_words = collections.Counter(word_list)
    print(f'Результат через Counter: {counter_words.most_common(10)}\nРезультат через мою функцию получения топ: ', end='')

    return word_list


def processing_xml(path):
    parser = ETS.XMLParser(encoding="cp1251")
    xmltree = ETS.parse(path, parser)

    xmlroot = xmltree.getroot()
    titles_list = xmlroot.findall('channel/item/title')
    word_list = []
    for title in titles_list:
        word_in_title = [word for word in title.text.lower().split(' ') if len(word) > 6]
        word_list.extend(word_in_title)

    return word_list


def processing_csv(path):
    word_list = []

    with open(path) as file:
        reader_csv = csv.reader(file)
        news_list = list(reader_csv)

    header = news_list.pop(0)
    title_index = header.index('title')
    for news in news_list:
        word_in_title = [word for word in news[title_index].lower().split(' ') if len(word) > 6]
        word_list.extend(word_in_title)

    return word_list


def main():
    name_of_files = [file for file in os.listdir(os.getcwd()) if 'newsafr' in file]

    for name_file in name_of_files:
        path = os.path.join(os.getcwd(), name_file)
        if '.json' in name_file:
            print('JSON: ', end='')
            processing_word_list(processing_json(path))
        elif '.xml' in name_file:
            print('XML: ', end='')
            processing_word_list(processing_xml(path))
        elif '.csv' in name_file:
            print('CSV: ', end='')
            processing_word_list(processing_csv(path))
        else:
            file_type = name_file.split('.')
            print(f'Разработчик еще не написал обработчик для {file_type[1]} формата данных')


if __name__ == '__main__':
    main()
