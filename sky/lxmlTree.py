import asciitree

class Node(object):
    def __init__(self, name, children):
        self.name = name
        self.children = children

    def __str__(self):
        return(self.name)
    
    def lineage(self):
        total = [self.name] + [y.name for y in self.children]
        for x in self.children:
            total += x.lineage()
        return(total)

def lxml_get_name(x, namedAttrs):
    my_string = x.tag
    if not isinstance(my_string, str):
        my_string = 'comment'
    if namedAttrs:
        for key, value in x.items():
            if key in namedAttrs:
                my_string += ', ' + key[0] + '=' + value
    return(my_string)        

def lxml_traverser(parent, graph, pruning, namedAttrs):
    graph = []        
    for x in parent:
        my_string = lxml_get_name(x, namedAttrs)
        graph.append(Node(my_string, lxml_traverser(x, graph, pruning, namedAttrs)))            
    if not pruning:
        return(graph)
    pruned_graph = []
    watcher = {}
    for x in graph:
        blood = "".join(x.lineage())
        if blood not in watcher:
            watcher[blood] = 1
        else:
            watcher[blood] += 1
    new_watcher = []
    for x in graph:        
        blood = "".join(x.lineage())
        if blood not in new_watcher:
            new_watcher.append(blood)
            pruned_graph.append(Node(x.name + " (" + str(watcher[blood]) + ")", x.children))
    return(pruned_graph)

def lxmlTree(lxmls, returning = False, printing = True, pruning = True, namedAttrs = None):
    if namedAttrs is None:
        namedAttrs = ['class', 'id']
    outps = []
    max_lens = 0
    if not isinstance(lxmls, list):
        lxmls = [lxmls]
    for num, lxml in enumerate(lxmls):
        z = lxml_traverser(lxml, [], pruning, namedAttrs)
        #outp = pinpoint(lxmls, num)
        outp = asciitree.draw_tree(Node(lxml_get_name(lxml, namedAttrs), z))
        max_lens = max(max_lens, max([len(x) for x in outp.split('\n')]))
        num += 1
        if num * (max_lens + 10) > 230:
            print('can only fit', num-1, 'out of', len(lxmls))
            break 
        outps.append(outp.split('\n'))
    newoutps = []    
    max_lines = max([len(x) for x in outps])
    for i in range(max_lines):
        tmp = ""
        for x in outps:
            # try: 
            tmp += '{:<{}}'.format(x[i], max_lens + 10) 
            # except:
                # tmp += '{:<{}}'.format('', max_lens + 10)
        newoutps.append(tmp)
    if printing:
        print('\n', "\n".join(newoutps))
    if returning:
        return("\n".join(newoutps))




import lxml.html

def add_depth(node, depth = 0, maxd = None):
    node.depth = depth
    if maxd is None:
        maxd = []
    else:
        maxd.append((node, node.depth)) 
    for n in node.iterchildren(): 
        add_depth(n , depth + 1, maxd)
    return maxd    

tree = lxml.html.fromstring('<html><body><div><a></a><h1></h1></div></body></html>')
            
z = add_depth(tree)

for x in tree.iter():
    print('wtf', x.depth)
