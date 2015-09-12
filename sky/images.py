# <figure> should maybe use some weighting
# background-url should also be allowed

# Also return most likely logo (logo, favicon??, first image?, icon)
import re


def general_ok_img(img_candidate, wrong_imgs):
    link = None
    if img_candidate.tag == 'img':
        if 'src' not in img_candidate.attrib:
            return False
        link = img_candidate.attrib['src']
    else:
        if 'content' in img_candidate.attrib:
            link = img_candidate.attrib['content']
        elif 'style' in img_candidate.attrib:
            tmp = re.findall(
                r'background-image:[ ]*url\((http[^)]+)', img_candidate.attrib['style'])
            if tmp:
                link = tmp[0]
    if link is None:
        return False
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


def dimensions_ok(img_candidate):
    try:
        if 'height' in img_candidate.attrib and int(img_candidate.attrib['height']) < 100:
            return False
        if 'width' in img_candidate.attrib and int(img_candidate.attrib['width']) < 100:
            return False
    except ValueError:
        pass
    return True


def get_images(tree, wrong_atts=None):
    if wrong_atts is None:
        wrong_atts = ['adsense', 'icon', 'logo', 'advert', 'toolbar', 'footer', 'layout', 'banner']
        # dit recoden in een tree.iter() loop, en dan ook de "node index"/num noteren hier.
    img_candidates = tree.xpath('//img[string-length(@src) > 3]')
    img_candidates += tree.xpath('//meta[contains(@property, "image")]')
    img_candidates += tree.xpath('//*[contains(@style, "background-image")]')
    leftover = []
    for img_candidate in img_candidates:
        if general_ok_img(img_candidate, wrong_atts):
            if img_candidate.tag == 'img':
                if dimensions_ok(img_candidate):
                    leftover.append(img_candidate)
            else:
                leftover.append(img_candidate)
    return leftover
