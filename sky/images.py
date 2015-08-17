## <figure> should also be considered
## background-url should also be allowed

## Also return most likely logo (logo, favicon??, first image?, icon)

def get_images(tree, wrong_imgs = None): 
    if wrong_imgs is None:
        wrong_imgs = ['adsense', 'icon', 'logo', 'advert', 'toolbar', 'footer', 'layout', 'banner'] 
    img_candidates = tree.xpath('//img[string-length(@src) > 3]')
    img_candidates += tree.xpath('//meta[contains(@property, "image")]')
    leftover = []
    for img_candidate in img_candidates: 
        if any([any([w in img_candidate.attrib[a] for w in wrong_imgs]) for a in img_candidate.attrib]):
            continue
        if img_candidate.tag == 'img':
            try:
                if 'height' in img_candidate.attrib and int(img_candidate.attrib['height']) < 25:
                    continue 
                if 'width' in img_candidate.attrib and int(img_candidate.attrib['width']) < 25:
                    continue 
            except ValueError: 
                pass
        leftover.append(img_candidate) 
    return leftover
