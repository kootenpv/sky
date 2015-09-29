import re

locale_US = {
    'symbol': r'\$',
    'currency': r'dollar[s]*',
    'units': [('million', 10**6),  ('m', 10**6), ('mn', 10**6), ('mil', 10**6),
              ('thousand', 10**3), ('k', 10**3),
              ('billion', 10**9), ('b', 10**9), ('bn', 10**9),
              ('cent', 0.01),
              ('\\b', 1), ('', 1)]}


class MoneyMatcher():

    def __init__(self, locale=None):
        if locale is None:
            locale = locale_US
        self.unit_dict = {}
        for k in locale['units']:
            self.unit_dict[k[0]] = k[1]
            self.unit_dict[k[0].title()] = k[1]
            self.unit_dict[k[0].upper()] = k[1]
        units = '({})'.format('|'.join([x[0] for x in locale['units']])) + '\\b'
        number_regex = '([0-9]*[,.]*[0-9]+[,.]*)'
        optional_space = '[ ]*'
        self.symbol = re.compile(locale['symbol'] + optional_space +
                                 number_regex + optional_space + units, re.IGNORECASE)
        self.currency = re.compile(number_regex + optional_space +
                                   units + optional_space + locale['currency'], re.IGNORECASE)

    def find(self, text, min_amount=0, max_amount=10**12):
        matches = []
        for m in self.symbol.finditer(text):
            matches.append([range(m.start(), m.end()), m.groups()])

        for m in self.currency.finditer(text):
            s = m.start()
            e = m.end()
            for mm in matches:
                if s in mm[0]:
                    mm[0] = range(mm[0].start, e)
                    break
                if e in mm[0]:
                    mm[0] = range(s, mm[0].stop)
                    break
            else:
                matches.append([range(m.start(), m.end()), m.groups()])

        results = [(text[x[0].start:x[0].stop], self.convertMatchToValue(
            x[1]), x[0].start, x[0].stop) for x in matches]

        return [r for r in results if min_amount < r[1] < max_amount]

    def convertMatchToValue(self, match):
        value = match[0].replace(',', '.').strip('.')
        modifier = 1000 ** (len(re.findall(r'\.\d{3}[^0-9]', value)) +
                            bool(re.search(r'\.\d{3}$', value)))
        value = float(value)
        unit_modifier = self.unit_dict[match[1]]
        return value * modifier * unit_modifier


def investment_annotation(title, body, money, entities, indicators=None,
                          max_char_distance=100):
    # Create annotation of (company, money) if they are within max_char_distance (title/body)
    # Only if "invest", "fund" or "rais" are found nearby as well.
    total_content = title + ' ' + body
    if indicators is None:
        indicators = ['Invest', 'Fund', 'Rais']
    indicators = list(set(indicators + [x.lower() for x in indicators]))
    entities_locations = [(e['text'], total_content.find(e['text']))
                          for e in entities if e['type'] in ['Person', 'Company']]
    indicator_locations = [(x, total_content.find(x))
                           for x in indicators if total_content.find(x) > -1]
    me_combinations = {}
    for m in money:
        for e in entities_locations:
            for i in indicator_locations:
                if abs(e[1] - m[1]) < max_char_distance and abs(e[1] - i[1]) < max_char_distance:
                    if m not in me_combinations:
                        me_combinations[m] = (e[0], abs(e[1] - m[1]))
                    elif abs(e[1] - m[1]) < me_combinations[m][1]:
                        me_combinations[m] = (e[0], abs(e[1] - m[1]))

    return [{'company': me_combinations[m][0], 'amount': m[1]} for m in me_combinations]
