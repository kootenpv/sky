import json
import translate

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

languages = ['aa','ab','af','ak','sq','am','ar','an','hy','as','av','ae','ay','az','ba','bm','eu','be','bn','bh','bi','bo','bs','br','bg','my','ca','cs','ch','ce','zh','cu','cv','kw','co','cr','cy','cs','da','de','dv','nl','dz','el','en','eo','et','eu','ee','fo','fa','fj','fi','fr','fr','fy','ff','ka','de','gd','ga','gl','gv','el','gn','gu','ht','ha','he','hz','hi','ho','hr','hu','hy','ig','is','io','ii','iu','ie','ia','id','ik','is','it','jv','ja','kl','kn','ks','ka','kr','kk','km','ki','rw','ky','kv','kg','ko','kj','ku','lo','la','lv','li','ln','lt','lb','lu','lg','mk','mh','ml','mi','mr','ms','mk','mg','mt','mn','mi','ms','my','na','nv','nr','nd','ng','ne','nl','nn','nb','no','ny','oc','oj','or','om','os','pa','fa','pi','pl','pt','ps','qt','qu','rm','ro','ro','rn','ru','sg','sa','si','sk','sk','sl','se','sm','sn','sd','so','st','es','sq','sc','sr','ss','su','sw','sv','ty','ta','tt','te','tg','tl','th','bo','ti','to','tn','ts','tk','tr','tw','ug','uk','ur','uz','ve','vi','vo','cy','wa','wo','xh','yi','yo','za','zh','zu']

answers = {}

for target in languages:
    answers[target] = {}
    for month in months: 
        try:
            answers[target][translate.translator('en', target, month)[0][0][0].lower()] = month
        except TypeError:
            print(target)    
            break

bad = []    
for a in answers:
    if not answers[a]:
        bad.append(a)

for a in bad:
    answers.pop(a)        
    
with open('date_translation_table.json', 'w', encoding='utf8') as json_file:
    json.dump(answers, json_file, ensure_ascii=False)
