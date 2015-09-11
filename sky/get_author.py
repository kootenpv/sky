# https://developer.ibm.com/bluemix/2015/09/09/bluemix-interactive-in-bangalore-abouthive/

import re
import json
import os
from pkg_resources import resource_filename

from sky.helper import get_text_and_tail

fname = os.path.abspath(resource_filename('sky.data', 'author_translation_table.json'))

with open(fname, encoding="utf-8") as f:
    author_translation_table = json.load(f)
    uppered = {x.title(): author_translation_table[x] for x in author_translation_table}
    author_translation_table.update(uppered)


def author_translation(txt, lang):
    if lang in author_translation_table:
        for month in author_translation_table[lang]:
            txt = txt.replace(month, author_translation_table[lang][month])
    return txt


def get_text_author(txt):
    res = re.findall(r"\b([A-Z][a-zA-Z' ]+)", txt)
    if res:
        for r in res:
            rsplit = r.split()
            if len(rsplit) < 6 and len(rsplit) > 1:
                return r.strip()
    return False


def get_author(tree, lang='en'):
    # Couple ways of matching:
    # - Both in meta and in text
    # - Node has one of the goods in it, text has it in it, and the case is authoric
    # - Node has one of the goods in it
    # - Text has one of the goods in it
    goods = ['author', 'by', 'publi', 'write', 'written', 'info']
    hard_authors = []
    meta_authors = []
    text_hard_authors = []
    text_soft_authors = []
    meta_nodes = tree.xpath('//head/meta')

    for option in goods:

        for meta in meta_nodes:
            if not any([option in a for a in meta.values()]):
                continue

            # dit gaat nog best helemaal fout! (ik moet atts nog chcken op goods)
            for attr in meta.attrib:
                author = get_text_author(author_translation(meta.attrib[attr], lang))
                if author:
                    meta_authors.append(author)

    for num, node in enumerate(tree.iter()):
        # hard author
        if not any([g in a for a in node.attrib.values() for g in goods]):
            for parent in node.iterancestors():
                attr_values = parent.attrib.values()
                if any([g in a for a in attr_values for g in goods]):
                    break
            else:
                continue
        tailtext = get_text_and_tail(node).strip()
        if tailtext and len(tailtext) < 200:
            if lang != 'en':
                tailtext = author_translation(tailtext, lang)
            hard_author = get_text_author(tailtext)
            if hard_author:
                hard_authors.append((num, hard_author))

    for num, node in enumerate(tree.iter()):
        tailtext = get_text_and_tail(node).strip()
        if tailtext and len(tailtext) < 200:
            res = re.findall(r"(author|Author|AUTHOR)[:;]* ([A-Z][a-zA-Z' ]+)", tailtext)
            if res:
                res = res[0]
                if res in meta_authors:
                    text_hard_authors.append((res, num))
                else:
                    text_soft_authors.append((res, num))
            else:
                res = re.findall(r"\b(by|By|BY)[:;]* ([A-Z][a-zA-Z' ]+)", tailtext)
                if res:
                    res = res[0]
                    if res in meta_authors:
                        text_hard_authors.append((res, num))
                    else:
                        text_soft_authors.append((res, num))

    hardest_authors = []
    not_hardest_authors = []
    for num, ha in hard_authors:
        if ha in meta_authors:
            hardest_authors.append((ha, num))
        else:
            not_hardest_authors.append((ha, num))

    meta_authors = set(meta_authors)

    return hardest_authors, not_hardest_authors, text_hard_authors, text_soft_authors, meta_authors
