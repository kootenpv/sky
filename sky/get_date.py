# issues

# [{'author': 'Charles Gross',
#   'related': ['http://www.benzinga.com/news/13/11/4070083/heartland-express-acquires-gordon-trucking-for-approximately-300m',
#    'http://www.benzinga.com/news/13/11/4071005/allot-receives-3m-initial-phase-order-from-tier-one-apac-operator-for-service-gat',
#    'http://www.benzinga.com/news/15/09/5868511/update-valeant-chair-ceo-pearson-issues-letter-to-employees-brings-up-recent-decl',
#    'http://www.benzinga.com/news/15/09/5875765/us-stock-futures-jump-adp-report-in-focus',
#    'http://www.benzinga.com/news/15/09/5875748/positive-data-presented-on-pieris-pharmaceuticals-inhaled-asthma-program-at-ers-a'],
#   'url': 'http://www.benzinga.com/news/13/11/4070252/marriott-to-replace-rangold-resources-in-nasdaq-100-index-beginning-november-18-2',
#   'images': [],
#   '_rev': '1-f0d089dd66503c5b1a4350f6a01968ca',
#   'body': ['Marriott International (NASDAQ: MAR) will become a component of the NASDAQ-100 Index and the NASDAQ-100 Equal Weighted Index prior to market open on Monday, November 18, 2013. Marriott International will replace Rangold Resources Limited (NASDAQ: GOLD).',
#    'Marriott International is headquartered in Bethesda, Maryland, and has a market capitalization of approximately $14.6 billion. For more information about the company, go to www.marriott.com.'],
#   'summary': '',
#   'scrape_date': '2015-09-30T12:10:07',
#   '_id': 'httpwwwbenzingacomnews13114070252marriott-to-replace-rangold-resources-in-nasdaq-100-index-beginning-november-18-2',
#   'crawl_date': '2015-09-30T12:10:07',
#   'language': 'en',
#   'title': 'Marriott to Replace Rangold Resources in NASDAQ-100 Index Beginning November 18, 2013',
#   'publish_date': '0100-11-18',
#   'money': [['$14.6 billion', 14600000000.0, 366, 379]],
#   'domain': 'http://www.benzinga.com'}]

import re
import json
import dateutil.parser
import datetime
import os

from sky.helper import get_text_and_tail

from pkg_resources import resource_filename
fname = os.path.abspath(resource_filename('sky.data', 'date_translation_table.json'))

with open(fname, encoding="utf-8") as f:
    date_translation_table = json.load(f)
    uppered = {x.title(): date_translation_table[x] for x in date_translation_table}
    date_translation_table.update(uppered)


class NoDefaultDate(object):
    """ Credits http://stackoverflow.com/a/18242643/1575066 """

    def replace(self, **fields):
        if any(f not in fields for f in ('year', 'month', 'day')):
            return None
        return datetime.datetime(2000, 1, 1).replace(**fields)


def patched_dateutil_parse(v, fuzzy):
    _actual = dateutil.parser.parse(v, default=NoDefaultDate(), fuzzy=fuzzy)
    if _actual is not None:
        # pylint: disable=E1101
        return _actual.date()
    else:
        return False


def date_translation(txt, lang):
    if lang in date_translation_table:
        for month in date_translation_table[lang]:
            txt = txt.replace(month, date_translation_table[lang][month])
    return txt


def get_text_date(v, fuzzy=False):
    try:
        for vv in v.replace('\xa0', ' ').split('|'):
            print(vv)
            d = patched_dateutil_parse(vv, fuzzy)
            return d
    except (ValueError, OverflowError, TypeError, AttributeError):
        return False


def within_years(d):
    return re.search(r'\b(19[89][0-9]|20[0-4][0-9])\b', d)


def get_dates(tree, titleind=(None, 1), lang='en'):
    # make this faster, its friggin slow (stupid fuzzy matching)
    hard_dates = []
    soft_dates = []
    fuzzy_hard_dates = []
    fuzzy_soft_dates = []
    meta_nodes = tree.xpath('//head/meta')

    goods = ['ublish', 'ublicat', 'date', 'time']

    for option in goods:

        for meta in meta_nodes:
            if not any([option in a for a in meta.values()]):
                continue

            for attr in meta.attrib:
                soft_dates.append(get_text_date(date_translation(meta.attrib[attr], lang)))

    for num, node in enumerate(tree.iter()):
        candi_dates = [v for k, v in node.items() if v and any([x in k for x in goods])]
        for v in candi_dates:
            if within_years(v):
                if lang != 'en':
                    v = date_translation(v, lang)
                d = get_text_date(v)
                if d:
                    soft_dates.append(d)
                else:
                    fuzzy_soft_dates.append(get_text_date(v, fuzzy=True))

        # hard date
        tailtext = get_text_and_tail(node).strip()
        if tailtext and within_years(tailtext):
            if lang != 'en':
                tailtext = date_translation(tailtext, lang)
            hard_date = get_text_date(tailtext)
            if hard_date:
                hard_dates.append((num, hard_date))
            else:
                fuzzy_hard_dates.append((num, get_text_date(tailtext, fuzzy=True)))

    soft_dates = set(soft_dates)
    fuzzy_soft_dates = set(x for x in fuzzy_soft_dates if x)
    fuzzy_hard_dates = [x for x in fuzzy_hard_dates if x]

    # Note that num and hd get switched here
    hardest_dates = []
    not_hardest_dates = []
    for num, hd in hard_dates:
        if hd in soft_dates:
            hardest_dates.append((hd, num))
        else:
            not_hardest_dates.append((hd, num))

    fuzzy_hardest_dates = []
    for num, hd in fuzzy_hard_dates:
        if hd in fuzzy_soft_dates:
            fuzzy_hardest_dates.append((hd, num))
        else:
            not_hardest_dates.append((hd, num))

    # if nothing, then try simply fuzzy on each node, and otherwise non fuzzy
    non_fuzzy_any = []
    fuzzy_any = []
    if not any([hardest_dates, fuzzy_hardest_dates, not_hardest_dates, soft_dates]):
        # no leads, try to parse everything non fuzzy
        for num, node in enumerate(tree.iter()):
            non_fuzzy_text = get_text_date(node, fuzzy=False)
            if non_fuzzy_text:
                non_fuzzy_any.append((non_fuzzy_text, num))
            else:
                fuzzy_text = get_text_date(node, fuzzy=True)
                if fuzzy_text:
                    fuzzy_any.append((fuzzy_text, num))

    date = ''
    date_node_index = None

    for dt in [hardest_dates, fuzzy_hardest_dates, not_hardest_dates,
               non_fuzzy_any, fuzzy_any]:
        if dt:
            date, date_node_index = sorted(dt, key=lambda x: abs(x[1] - titleind[1]))[0]
            break

    if not date and soft_dates:
        for sd in soft_dates:
            date = sd
            break

    all_dates = [hardest_dates, fuzzy_hardest_dates, not_hardest_dates, non_fuzzy_any, fuzzy_any]

    if date_node_index is not None:
        # It goes wrong when some year is mentioned in the title, then it removes title
        # print('removing date content', node.text) ...... is dit nog gerecent?
        date_node_indices = [[y[1] for y in x if y[0] == date] for x in all_dates]
        date_node_indices = [item for sub in date_node_indices for item in sub]
        for num, node in enumerate(tree.iter()):
            if num in date_node_indices:
                # maybe i now remove too littlet
                tt = get_text_and_tail(node)
                if tt and len(tt) < 25 or '|' in tt and len(tt) < 50:
                    node.text = ''
                    node.tail = ''
    return date


# testcases:
# 'http://finextra.com/news/fullstory.aspx?newsitemid=5235'
