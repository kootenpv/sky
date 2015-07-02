
def get_template_elements(tree):
    z = set()
    for x in tree.iter():
        if x.attrib:
            for a in x.attrib:
                z.add((x.tag, a, x.attrib[a], get_text_and_tail(x)))
    return z
        
