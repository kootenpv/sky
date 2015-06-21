from nltk.corpus import stopwords

def generate_testables(words, stopword_set, n_grams = 4):
    grams = set()
    n = len(words)
    for i in range(len(words)):
        for j in range(n_grams):
            if n - j > i:
                word_list = [x.lower() for x in words[i : i + j + 1]]
                if any([len(x) < 3 for x in word_list]):
                    continue
                if set(word_list) & stopword_set:
                    continue
                grams.add(" ".join(word_list))
    return grams            

def get_dbpedia_from_words(words, db_dict, ok_entities = None):
    if ok_entities is None:
        ok_entities = ['Person', 'Organisation']
    ws = generate_testables(words, stopset)
    classes = [] 
    for x in ws:
        if x in db_dict: 
            for y in db_dict[x]:
                if y in ok_entities:
                    classes.append(('db_' + y, x))
                    break 
    return classes

    
stopset = set(stopwords.words('english'))    
