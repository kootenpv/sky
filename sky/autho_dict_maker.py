import os
import json
import translate

phrases = ['author', 'by', 'publi', 'write', 'written', 'info']

languages = ['aa','ab','af','ak','sq','am','ar','an','hy','as','av','ae','ay','az','ba','bm','eu','be','bn','bh','bi','bo','bs','br','bg','my','ca','cs','ch','ce','zh','cu','cv','kw','co','cr','cy','cs','da','de','dv','nl','dz','el','en','eo','et','eu','ee','fo','fa','fj','fi','fr','fr','fy','ff','ka','de','gd','ga','gl','gv','el','gn','gu','ht','ha','he','hz','hi','ho','hr','hu','hy','ig','is','io','ii','iu','ie','ia','id','ik','is','it','jv','ja','kl','kn','ks','ka','kr','kk','km','ki','rw','ky','kv','kg','ko','kj','ku','lo','la','lv','li','ln','lt','lb','lu','lg','mk','mh','ml','mi','mr','ms','mk','mg','mt','mn','mi','ms','my','na','nv','nr','nd','ng','ne','nl','nn','nb','no','ny','oc','oj','or','om','os','pa','fa','pi','pl','pt','ps','qt','qu','rm','ro','ro','rn','ru','sg','sa','si','sk','sk','sl','se','sm','sn','sd','so','st','es','sq','sc','sr','ss','su','sw','sv','ty','ta','tt','te','tg','tl','th','bo','ti','to','tn','ts','tk','tr','tw','ug','uk','ur','uz','ve','vi','vo','cy','wa','wo','xh','yi','yo','za','zh','zu']

answers = {}

for target in languages:
    answers[target] = {}
    for phrase in phrases: 
        try:
            answers[target][translate.translator('en', target, phrase)[0][0][0].lower()] = phrase
        except TypeError:
            print(target)    
            break

bad = []    
for a in answers:
    if answers[a]:
        for k in answers[a]:
            if k in phrases: 
                print('bad', a, k) 
                bad.append((a,k))

for a in bad:
    answers[a[0]].pop(a[1])
                
bad = []    
for a in answers:
    if not answers[a]:
        print('bad', a)
        bad.append(a)

for a in bad:
    answers.pop(a)        

fname = os.path.join(os.path.dirname(__file__), '/data/author_translation_table.json')    

with open(fname, 'w', encoding='utf8') as json_file:
    json.dump(answers, json_file, ensure_ascii=False)

    
