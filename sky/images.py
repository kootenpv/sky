# <figure> should also be considered
# background-url should also be allowed

# Also return most likely logo (logo, favicon??, first image?, icon)


def general_ok_img(img_candidate, wrong_imgs):
    if img_candidate.tag == 'img':
        if 'src' not in img_candidate.attrib:
            return False
        link = img_candidate.attrib['src']
    else:
        if 'content' not in img_candidate.attrib:
            return False
        link = img_candidate.attrib['content']
    # if link longer than 1000 chars, drop it
    if len(link) > 1000:
        return False
    # if link does not start with "http", drop it
    if not link.startswith('http'):
        return False
    # if link attributes contain one of the wrong atts, drop it
    if any([any([w in img_candidate.attrib[a] for w in wrong_imgs])
            for a in img_candidate.attrib]):
        return False
    return True


def img_ok(img_candidate):
    try:
        if 'height' in img_candidate.attrib and int(img_candidate.attrib['height']) < 25:
            return False
        if 'width' in img_candidate.attrib and int(img_candidate.attrib['width']) < 25:
            return False
    except ValueError:
        pass
    return True


def get_images(tree, wrong_atts=None):
    if wrong_atts is None:
        wrong_atts = ['adsense', 'icon', 'logo', 'advert', 'toolbar', 'footer', 'layout', 'banner']
    img_candidates = tree.xpath('//img[string-length(@src) > 3]')
    img_candidates += tree.xpath('//meta[contains(@property, "image")]')
    leftover = []
    for img_candidate in img_candidates:
        if general_ok_img(img_candidate, wrong_atts):
            if img_candidate.tag == 'img':
                if img_ok(img_candidate):
                    leftover.append(img_candidate)
            else:
                leftover.append(img_candidate)
    return leftover
