#!/usr/bin/env python3
import bs4
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


def get_name(x, namedAttrs):
    my_string = "".join(x.name.split())
    if namedAttrs:
        for att in namedAttrs:
            if att in x.attrs:
                my_string += ', ' + att[0] + '=' + "".join(x.attrs[att])
    return(my_string)


def traverser(parent, graph, pruning, namedAttrs):
    graph = []
    for x in parent:
        if isinstance(x, bs4.element.Tag):
            my_string = get_name(x, namedAttrs)
            graph.append(Node(my_string, traverser(x, graph, pruning, namedAttrs)))
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


def soupTree(soups, returning=False, printing=True, pruning=True, namedAttrs=None):
    if namedAttrs is None:
        namedAttrs = ['class', 'id']
    outps = []
    max_lens = 0
    if not isinstance(soups, list):
        soups = [soups]
    for num, soup in enumerate(soups):
        parent = soup.children
        z = traverser(parent, [], pruning, namedAttrs)
        outp = asciitree.draw_tree(Node(get_name(soup, namedAttrs), z))
        max_lens = max(max_lens, max([len(x) for x in outp.split('\n')]))
        num += 1
        if num * (max_lens + 10) > 230:
            print('can only fit', num - 1, 'out of', len(soups))
            break
        outps.append(outp.split('\n'))
    newoutps = []
    max_lines = max([len(x) for x in outps])
    for i in range(max_lines):
        tmp = ""
        for x in outps:
            try:
                tmp += '{:<{}}'.format(x[i], max_lens + 10)
            except:
                tmp += '{:<{}}'.format('', max_lens + 10)
        newoutps.append(tmp)
    if printing:
        print('\n', "\n".join(newoutps))
    if returning:
        return("\n".join(newoutps))
