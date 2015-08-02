import justext

def justy(html, lang = 'en'):
    lang = {'en' : 'english', 'nl' : 'dutch'}[lang]
    jt = justext.justext(html, justext.get_stoplist(lang))
    return jt

def justyTitle(jt):
    res = [x.text for x in jt if x.is_heading and not x.is_boilerplate]
    if res:
        return res[0]
    return ''

def justyBody(jt):
    res = [x.text for x in jt if not x.is_heading and not x.is_boilerplate]
    return '\n'.join(['<p>{}</p>'.format(x) for x in res])
    
    
