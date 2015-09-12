import os

try:
    from nltk.corpus import stopwords
    stopset = set(stopwords.words('english'))
except ImportError:
    print("Cannot use dbpedia without 'pip install nltk'")

try:
    import ujson as json
except ImportError:
    import json


def generate_testables(words, stopword_set, n_grams=4):
    grams = set()
    n = len(words)
    for i in range(len(words)):
        for j in range(n_grams):
            if n - j > i:
                ws = words[i: i + j + 1]
                if any(['NN' not in x[1] for x in ws]):
                    continue
                word_list = [x[0].lower() for x in ws]
                if any([len(x) < 3 for x in word_list]):
                    continue
                if set(word_list) & stopword_set:
                    continue

                grams.add((" ".join([x[1] for x in ws]), " ".join(word_list)))
    return grams


def get_dbpedia_from_words(pos_tags, db_dict, ok_entities=None):
    if ok_entities is None:
        ok_entities = ['Person', 'Organisation']
    ws = generate_testables(pos_tags, stopset)
    classes = []
    for x in ws:
        if x[1] in db_dict:
            for y in db_dict[x[1]]:
                if y in ok_entities:
                    classes.append(('db_' + y + '_' + x[0], x))
                    break
    return classes


def load_dbpedia():
    # looks for 'dbpedia.json'; sky/sky/dbpedia.json
    with open(os.path.join(os.path.dirname(__file__), 'dbpedia.json')) as f:
        return json.load(f)
