import nltk

def extract_entities(text):
    results = []
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                results.append((chunk.label(), ' '.join(c[0] for c in chunk.leaves())))
    return results
