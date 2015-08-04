import requests
import json

def call_opener(text, opener_method): 
    template_url = 'http://opener.olery.com/{}'
    return requests.post(template_url.format(opener_method), data = {'input' : text}).text

def chained_call(text, opener_methods): 
    for opener_method in opener_methods:
        text = call_opener(text, opener_method)
    return text    
            
def langid(text):
    return call_opener(text, 'language-identifier')

def pos_tag(text):
    return call_opener(call_opener(langid(text), 'tokenizer'), 'pos-tagger')

def ned(text):
    return call_opener(call_opener(pos_tag(text), 'ner'), 'ned')

def kaf2json(text):
    return call_opener(text, 'kaf2json')

def json_ned(text):
    return json.loads(kaf2json(ned(text)))

def get_entities(text):
    return sorted(json_ned(text)['entities'].values(), key = lambda x: int(x['terms'][0][1:]))

def pretty_print_entities(text):
    print(json.dumps(get_entities(text), indent=4, separators=(',', ': ')))

# def reduced_get_entities(text):
#     entities = get_entities(text)
#     texts = set([e['text'] for e in entities])
#     should_disappear = set([x for x in texts if any(x in y for y in texts if x != y)])
#     return [e for e in entities if e['text'] not in should_disappear and e['type'] in ['PERSON', 'ORGANIZATION']]
    
    
    
    
####### clues:

# 'emphasize', 'tell', 'said', 'co-founder', 'CEO', 'managing director of', 'watchmaker' <name>,

# <quote> <person> <role> <company> <said/told>

# 'partnering'
# <C> engineers, <C> employees

# 'CapCap' invests

# <the> <thing>

# company, a <location> based

# find all indicators
# all single capital words not starting a sentence --> companies
# resolve 
