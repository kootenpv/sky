import dateutil.parser
import json
from datetime import date

with open('date_translation_table.json') as f:
    date_translation = json.load(f)

def translate_months(txt):
    lang = langdetect.detect(txt)
    txt = txt.lower()
    if lang in date_translation:
        for month in date_translation[lang]:
            txt = txt.replace(month, date_translation[lang][month])
    return txt        

def get_publish_from_meta(tree):
    dates = [] 
    meta_nodes = tree.xpath('//head/meta')

    for option in ['ublish', 'ublicat', 'date']: 
        
        for meta in meta_nodes:
            if not option in meta.attrib:
                continue

            for attr in meta.attrib:
                try:
                    d = dateutil.parser.parse(meta.attrib[attr])
                    dates.append(d)
                except (ValueError, OverflowError):
                    pass
            
    return dates 

def get_date_from_content(html):
    date_txt = translate_months(html)
    options = [date_txt[m.start() - 20 : m.end() + 20] for m in re.finditer('20[0-9]{2}', date_txt)]
    for option in options: 
        try:
            d = dateutil.parser.parse(option)
            if d != sucky_default: 
                print(d)
        except (ValueError, OverflowError):
            pass    
    return options
