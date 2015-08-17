### sky

Installation summary (note: sky/sky/ is different from sky/):

- if it is the first time using tldextract, run: `python3 -c "import tldextract; tldextract.extract('http://google.nl')"` to load Top Level Domain extracts
- Create cloudant.username (in /path/to/clone/sky/sky/)
- Create cloudant.password (in /path/to/clone/sky/sky/)
- Go to the [document "default"](https://835ea05b-d4b0-4210-a9f7-f838266e65d0-bluemix.cloudant.com/dashboard.html#database/crawler-plugins/default), and change `collections_path` to the path where you want to store HTML locally. Make sure this is an existing directory (e.g. /Users/taco/rabo_collections)

#### Installation

The following should be done:

```python
pip3 install sky
```

This will install some lovely packages.

If it is the first time using tldextract, run: `python3 -c "import tldextract; tldextract.extract('http://google.nl')"` to load Top Level Domain extracts.CC

To make a connection with Cloudant, put `cloudant.password` and `cloudant.username` single line files in `..../sky/sky/.` 

For now, go to Cloudant, visit database `crawler-plugins`, [go to the document "default"](https://835ea05b-d4b0-4210-a9f7-f838266e65d0-bluemix.cloudant.com/dashboard.html#database/crawler-plugins/default), and change `collections_path` to the path where you want to store HTML locally.

### Usage

To create a crawler, a crawler config has to be uploaded to Cloudant to the crawler-plugins database. 

#### Create config

If we want to for example crawl games-news from nu.nl (http://www.nu.nl/games/), we can use the following config:

```python
config = {
  "seed_urls": [
    "http://www.nu.nl/games"
  ],
  "collection_name": "nu.nl",
  "crawl_filter_strings": [],
  "crawl_required_strings": [
    'games/'
    ],
  "index_filter_strings": [],
  "index_required_strings": [
    "games/"
  ]
}
```

**Important**: whenever a crawl is being done, first the "[default](https://835ea05b-d4b0-4210-a9f7-f838266e65d0-bluemix.cloudant.com/dashboard.html#database/crawler-plugins/default)" (project-based) config is loaded, after which the specific named plugin config overwrites all the settings. For example, the default is to save a maximum amount of 1000000 responses. In testing plugin "nu.nl", you can overwrite this (advised) to only `max_saved_responses : 100`. See our Technical Design for a full specification of all the options available.

### Uploading a config to Cloudant

```python
from sky.crawler_plugins import CrawlCloudantPlugin
ccp = CrawlCloudantPlugin(plugin_name)
ccp.save_config(config)

# optionally it can be run immediately:
ccp.run()
```

#### Run config

Run a config by its plugin_name (crawler-plugin "id"):

```python
ccp = CrawlCloudantPlugin(plugin_name)
ccp.run()
```

Optionally it is possible to use the local cache (`ccp.run(use_cache=True)`). If you want to change anything in the settings that changes the crawling rules / indexing rules, you'll have to delete to local cache folder that has been created.

### Bad crawl/index settings

After crawling, it is recommended to check the summary of potential bad paths. For title, body, publish_date, and url the shortest (five) values are sorted so it can give a suggestion about which paths might be bad. (reasoning: if a title is really short or non existent, most likely it is a document that should be filtered)

```python
ccp = CrawlCloudantPlugin(plugin_name)
ccp.get_bad_documents()
```