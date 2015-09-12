from sky.configs import DEFAULT_CRAWL_CONFIG
from sky.scraper import Scraper
from sky.crawler import crawl

# Crawling
CRAWL_CONFIG = DEFAULT_CRAWL_CONFIG
CRAWL_CONFIG.update({
    'seed_urls': [
        'http://www.techcrunch.com/'
    ],

    'collections_path': '/Users/pascal/GDrive/sky_collections',

    'collection_name': 'techie',

    # Optional

    'crawl_filter_regexps': [

    ],

    'crawl_required_regexps': [
        '2015', '2014'
    ],

    'index_filter_regexps': [

    ],

    'index_required_regexps': [
        '2015', '2014'
    ],

    'max_saved_responses': 100,

    'max_workers': 10,
})

crawl.start(CRAWL_CONFIG)

# Indexing

SCRAPE_CONFIG = CRAWL_CONFIG.copy()

SCRAPE_CONFIG.update({
    'template_proportion': 0.09,
    'max_templates': 1000
})

skindex = Scraper(SCRAPE_CONFIG)

skindex.load_local_pages()
skindex.add_template_elements()

res = skindex.process_all(remove_visuals=True)
