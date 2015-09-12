import langdetect


def get_language(tree, headers, domain=None):
    lang = None

    if headers and 'content-language' in headers:
        lang = headers['content-language']

    if lang is None and 'lang' in tree.attrib:
        lang = tree.attrib['lang']

    if lang is None:
        page_txt = ' '.join(tree.xpath('//p/text()')) + ' '.join(tree.xpath('//div/text()'))
        if not page_txt:
            page_txt = tree.text_content()
        lang = langdetect.detect(page_txt)

    # Note that this won't work with weird domain names. A mapping is needed
    # from domain names to languages.
    if lang is None and domain is not None:
        lang = domain.split('.')[-1]
        if lang == 'com':
            return 'en'

    return lang[:2] or 'en'
