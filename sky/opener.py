import requests
import json


def call_opener(text, opener_method):
    template_url = 'http://opener.olery.com/{}'
    return requests.post(template_url.format(opener_method), data={'input': text}).text


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
    return sorted(json_ned(text)['entities'].values(), key=lambda x: int(x['terms'][0][1:]))


def pretty_print_entities(text):
    print(json.dumps(get_entities(text), indent=4, separators=(',', ': ')))

# def reduced_get_entities(text):
#     entities = get_entities(text)
#     texts = set([e['text'] for e in entities])
#     should_disappear = set([x for x in texts if any(x in y for y in texts if x != y)])
# return [e for e in entities if e['text'] not in should_disappear and
# e['type'] in ['PERSON', 'ORGANIZATION']]


# clues:

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


# jruby -S language-identifier
# jruby -S tokenizer
# jruby -S pos-tagger
# jruby -S tree-tagger
# jruby -S polarity-tagger
# jruby -S property-tagger
# jruby -S constituent-parser
# jruby -S ner
# jruby -S coreference
# jruby -S ned
# jruby -S opinion-detector
# jruby -S opinion-detector-basic
# jruby -S kaf2json
# jruby -S outlet
# jruby -S scorer


# echo "They're offering $1.5 million in grants, and their first project
# is a Science Learning Challenge. That's for companies and nonprofits
# that are building tech to help students develop science and engineering
# skills. They'll pick up to 15 challenge winners with grants that range
# from $50,000 to $150,000. While we've seen literacy efforts and math
# kick up in the last few years, we'd like to see that same vibrancy in
# science education, said Stacey Childress, CEO of NewSchools Venture
# Fund. The ed tech that we like to fund is synergistic. It blends the
# best of technology with live instruction and immersive and engaging
# content. Along with the capital, NewSchools is working with a nonprofit
# research group called WestEd to provide design feedback and
# recommendations based on what educational research suggests will work
# best. They'll build small-scale studies to test usability and
# feasibility in the classroom. Childress said that NewSchools is in the
# process of raising another $60 million philanthropic fund over the next
# three years. They've had several funds over the organization's life
# since 1998 that range from a few million dollars to $75 million. Through
# that capital, the organization has supported about 442 charter schools
# throughout the country, serving 171,000 kids. Generally, they've backed
# educational entrepreneurs creating new schools, but they also want to
# fund technical teams building software and tools, as well. That's what
# this new accelerator is about. This is just the first part of what we're
# doing in this area, Childress said. We want to invest in ed tech and
# identify market gaps like the ones in science we were just talking
# about." | /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S
# language-identifier | /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S
# tokenizer | /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S
# pos-tagger | /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S ner


# txt="""They're offering $1.5 million in grants, and their first project is a Science Learning Challenge. That's for companies and nonprofits that are building tech to help students develop science and engineering skills. They'll pick up to 15 challenge winners with grants that range from $50,000 to $150,000. While we've seen literacy efforts and math kick up in the last few years, we'd like to see that same vibrancy in science education, said Stacey Childress, CEO of NewSchools Venture Fund. The ed tech that we like to fund is synergistic. It blends the best of technology with live instruction and immersive and engaging content. Along with the capital, NewSchools is working with a nonprofit research group called WestEd to provide design feedback and recommendations based on what educational research suggests will work best. They'll build small-scale studies to test usability and feasibility in the classroom. Childress said that NewSchools is in the process of raising another $60 million philanthropic fund over the next three years. They've had several funds over the organization's life since 1998 that range from a few million dollars to $75 million. Through that capital, the organization has supported about 442 charter schools throughout the country, serving 171,000 kids. Generally, they've backed educational entrepreneurs creating new schools, but they also want to fund technical teams building software and tools, as well. That's what this new accelerator is about. This is just the first part of what we're doing in this area, Childress said. We want to invest in ed tech and identify market gaps like the ones in science we were just talking about."""


# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-tree-tagger && \
# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-polarity-tagger && \
# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-property-tagger && \
# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-constituent-parser && \
# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-ner && \
# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-coreference && \
# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-ned && \
# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-opinion-detector && \
# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-opinion-detector-basic && \
# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-kaf2json && \
# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-outlet && \
# /Users/pascal/Downloads/jruby-9.0.0.0/bin/jruby -S gem install opener-scorer
