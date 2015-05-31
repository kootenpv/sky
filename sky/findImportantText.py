tr = Training("nieuwsdumper-testcase1", "/Users/pascal/GDrive/virtual-python/sky/sky/tests/").load()

t1 = set([x.text_content() for x in tr.trees[0].iter()])
t2 = set([x.text_content() for x in tr.trees[1].iter()])
t3 = set([x.text_content() for x in tr.trees[1].iter()])

y = list(t1.difference(t2).difference(t3))
y1 = list(t2.difference(t1).difference(t3))



it = 0
res = []
for i in range(len(y)):
    single = True
    for j in range(i, len(y)):
        if i < j:
            if y[i] not in y[j]:
                single = False
    if single:
        res.append(y[i])            
