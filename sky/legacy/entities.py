import nltk

def extract_entities(blob):
    results = []
    for chunk in nltk.ne_chunk(nltk.pos_tag(blob.words)):
        if hasattr(chunk, 'label'):
            results.append((chunk.label(), ' '.join(c[0] for c in chunk.leaves())))
    return results
