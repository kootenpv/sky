DEFAULT_CRAWL_CONFIG = {
    # Required
    'seed_urls': [

    ],

    'collections_path': '',

    'collection_name': '',

    # Optional

    'crawl_filter_regexps': [

    ],

    'crawl_required_regexps': [
    ],

    'index_filter_regexps': [

    ],

    'index_required_regexps': [

    ],

    'bad_xpaths': [

    ],

    'max_redirects_per_url': 10,

    'max_tries_per_url': 3,

    'max_workers': 5,

    'max_saved_responses': 20,

    'login_url': '',
    'login_data': {},

    "logging_level": 2,
    # Unimplemented
    'max_hops': 10,

    # Scrape stuff"
    'template_proportion': 0.09,
    'max_templates': 1000
}

PRODUCTION_CRAWL_CONFIG = DEFAULT_CRAWL_CONFIG.copy()

PRODUCTION_CRAWL_CONFIG.update({
    'max_saved_responses': 1000000000,
    'max_hops': 100,
    'max_workers': 100
})
