import re
import json
import dateutil.parser

with open('date_translation_table.json') as f:
    date_translation_table = json.load(f)

import datetime


class NoDefaultDate(object): 
    """ Credits http://stackoverflow.com/a/18242643/1575066 """
    def replace(self, **fields):
        if any(f not in fields for f in ('year', 'month', 'day')):
            return None
        return datetime.datetime(2000, 1, 1).replace(**fields)
        
def patched_dateutil_parse(v):
    _actual = dateutil.parser.parse(v, default=NoDefaultDate())
    if _actual is not None:
        # pylint: disable=E1101
        return _actual.date()
    else:
        return False
    
def date_translation(txt, lang): 
    txt = txt.lower()
    if lang in date_translation_table:
        for month in date_translation[lang]:
            txt = txt.replace(month, date_translation[lang][month])
    return txt        

def get_publish_from_meta(tree):
    dates = [] 
    meta_nodes = tree.xpath('//head/meta')

    for option in ['ublish', 'ublicat', 'date']: 
        
        for meta in meta_nodes:
            if not any([option in a for a in meta.values()]):
                continue

            for attr in meta.attrib:
                try:
                    d = patched_dateutil_parse(meta.attrib[attr])
                    dates.append(d)
                except (ValueError, OverflowError):
                    pass
            
    return dates 

def get_date_from_content(html, lang):
    date_txt = date_translation(html, lang)
    options = [date_txt[m.start() - 20 : m.end() + 20] for m in re.finditer('20[0-9]{2}', date_txt)]
    for option in options: 
        try:
            d = patched_dateutil_parse(option)
            print(d)
        except (ValueError, OverflowError):
            pass    
    return options
