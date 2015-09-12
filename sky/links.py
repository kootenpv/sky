# Link('http://nu.nl/nieuws', slugified = 'httpnunlnieuws', parent =
# 'http://nu.nl', hop = 1, refTo, refFrom)

import re


def get_word_set(url):
    question_mark_index = url.find('?')
    url = url[:question_mark_index] if question_mark_index > -1 else url
    return set(re.split('[^a-zA-Z0-9]', url))


def get_similarity(url1, ws2, sc2):
    ws1 = get_word_set(url1)
    if ws1 == ws2:
        return (0, 0)
    return - abs(url1.count('/') - sc2), len(ws1 & ws2) / len(ws2)


def get_sorted_links(urls, request_url):
    wsr = get_word_set(request_url)
    slash_count = request_url.count('/')
    return sorted(set(urls), key=lambda u: get_similarity(u, wsr, slash_count), reverse=True)
