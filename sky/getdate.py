import dateutil.parser as dparser


bla = str(tree.xpath('/html')[0].text_content())

dates = set()
for i in range(0, len(bla), 1000):
    try:
        dates.add(dparser.parse(bla[i-20:i+20], fuzzy=True))
    except Exception as e:
        print('EXCEPTION', e)    

    
