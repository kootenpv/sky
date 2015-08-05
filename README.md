### sky

Installation summary:

- git clone https://github.com/kootenpv/sky
- cd sky/sky
- pip install -r requirements.txt
- export PYTHONPATH=$PYTHONPATH:/path/to/this/clone/sky
- Create cloudant.username (in /path/to/clone/sky/sky/)
- Create cloudant.password (in /path/to/clone/sky/sky/)
- Go to the [document "default"](https://835ea05b-d4b0-4210-a9f7-f838266e65d0-bluemix.cloudant.com/dashboard.html#database/crawler-plugins/default), and change `collections_path` to the path where you want to store HTML locally.

#### Installation

The following should be done:

```python
pip install -r requirements.txt
```

Make sky available globally by adding:

```python
export PYTHONPATH=$PYTHONPATH:/path/to/this/clone/sky
```

to your `.bashrc`

or instead on a "per session basis" use:

```python
import sys
sys.path.append('/path/to/this/clone/sky')
```

at the top of a script to be able to `import sky`.

To make a connection with Cloudant, put `cloudant.password` and `cloudant.username` single line files in `..../sky/sky/.` 

For now, go to Cloudant, visit database `crawler-plugins`, [go to the document "default"](https://835ea05b-d4b0-4210-a9f7-f838266e65d0-bluemix.cloudant.com/dashboard.html#database/crawler-plugins/default), and change `collections_path` to the path where you want to store HTML locally.

### Usage

To create a crawler, a crawler config has to be uploaded to Cloudant to the crawler-plugins database. 

#### Create config

If we want to for example crawl http://www.nu.nl/games, we can use the following config:

```python
config = {
  "seed_urls": [
    "http://www.emerce.nl/"
  ],
  "collection_name": "emerce.nl",
  "crawl_filter_strings": [],
  "crawl_required_strings": [],
  "index_filter_strings": [],
  "index_required_strings": [
    "nieuws/"
  ]
}
```

**Important**: whenever a crawl is being done, first the "default" (project-based) config is loaded, after which the specific named plugin config overwrites all the settings. For example, the default is to save a maximum amount of 1000000 responses. In testing plugin "nu.nl", you can overwrite this (advised) to only `max_saved_responses : 100`. See our Technical Design for a full specification of all the options available.

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