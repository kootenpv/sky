import re

def get_word_set(url): 
    question_mark_index = url.find('?')
    url = url[:question_mark_index] if question_mark_index > -1 else url
    return set(re.split('[a-zA-Z0-9]', url))

def get_similarity(url1, ws2):
    ws1 = get_word_set(url1) 
    if ws1 == ws2:
        return 0
    return 2 * len(ws1 & ws2) / (len(ws1) + len(ws2))
    
def get_sorted_links(urls, request_url):
    wsr = get_word_set(request_url)
    return sorted(set(urls), key = lambda u: get_similarity(u, wsr), reverse = True) 
    

    
    
    
