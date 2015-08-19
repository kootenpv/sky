### sky

sky is a web scraping framework, implemented with the latest python versions in mind (3.4+). It uses the asynchronous `asyncio` framework, as well as many popular modules and extensions.

Most importantly, it aims for **next generation** web crawling where machine intelligence is used to speed up the development/maintainance/reliability of crawling.

It mainly does this by considering the user to be interested in content from *domains*, not just a collection of *single pages*.

It would allow it to:
- Drop duplicate content (menus, texts, images)
- Detect whether a website changed the layout (causing other scrapers to fail)
- Understand sections of a website, such as comments, forum posts, related links etc
- Consider which pages are linked to which (star graph)
- Figure out the content pages by just pointing at the domain
- Relate pages (page A is related by content to page B)
- Consider an optimal re-crawling path
- Provide error checking tools (making sure no bad documents slip by)

Extending the project with Natural Language Processing is a next step. For example, there are steps to automatically detect acquisitions; `Company A acquires Company B`, and investments: `Company A invests B millions in Company C`.

#### Features/Goals

- **Really fast**, due to Python 3.4+ new asyncio/aiohttp libraries
- **Smart**, due to considering crawling of *websites* instead of single *pages*
- **Link-graph-analysis**, find out how a domain "looks" like
- **Boilerplate FREE**, removes crappy content (images, text, etc) that does not belong on pages
- **Nice API**, carefully crafted, easily extendible
- **Open-source**, democracy driven, with actual support
- **Free**, versus enormous costs for even medium scale projects using (worse) online services

See it live in action with a news website you propose!

#### Installation

Use pip to install sky:

```python
pip3 install sky
```

This will install only the required packages. Optional packages are for backends, such as elasticsearch, cloudant and ZODB. Storing data on the local system does not require any packages.

### Usage

# ******************* important to have a quick demo, and an extensive "Start your project"

- Online Demo
- Show me some code
- Show me some code with explanations

To start crawling, first a project has to be defined, a backend has to be picked, and a crawler class chosen.

#### Setup

```python
from sky.crawler_services import CrawlFileService
from sky.crawler_plugins import CrawlFilePluginNews
PROJECT_NAME = 'testproj'
storage_object = {'path' : '/Users/pascal/sky_collections/'}
cs = CrawlFileService(PROJECT_NAME, storage_object, CrawlFilePluginNews)
```

By creating this Service, the file paths will be initialized on the local system:

    /Users/pascal/sky_collections/testproj-crawler-plugins
    /Users/pascal/sky_collections/testproj-crawler-documents
    /Users/pascal/sky_collections/testproj-crawler-template_dict

#### Create default config

Whenever a crawl is being done, first the "default" (project-based) config is loaded, after which the specific named plugin config overwrites all the settings. For example, the default could be to save a maximum amount of 20 responses. However, if it would be wanted to extract a huge number of pages, it could be overwritten to `max_saved_responses : 10000000`.

Let's first define the default project config:

```python
from sky.configs import DEFAULT_CRAWL_CONFIG
default = cs.get_crawl_plugin('default')
default.save_config(DEFAULT_CRAWL_CONFIG)
```

See the [configs](https://github.com/kootenpv/sky/blob/master/sky/configs.py) file for a full specification of all the options available, as well as some example configs.

The `save_config` method will store a config file in the storage backend, in this case the `default` plugin.

### Adding a new crawl

If we want to for example crawl *europe* related news from bbc.com (http://www.bbc.com/news/world/europe), we can use the following config:

```python
bbc_config = {
    'seed_urls' : ['http://www.bbc.com/news/world/europe'],
    'crawl_required_strings' : ['europe'],
    'index_required_strings' : ['news/world-europe-'],
    'max_saved_responses' : 100, 
}
bbc = cs.get_crawl_plugin('bbc.com')
bbc.save_config(bbc_config)
```

Options explained:

- `'seed_urls' : ['http://www.bbc.com/news/world/europe']` is from where the crawl starts.
- `'crawl_required_strings' : ['europe']` will ensure we only visit URLs containing the word `europe`.
- `'index_required_strings' : ['news/world-europe-']` will only save/use pages with URLs that contain `news/world-europe-`.

This time, save_config saves the `bbc.com` specific configuration.

#### Run the crawler

Finally, run a config by its plugin_name (crawler-plugin "id"):

```python
cs.run('bbc.com')
```

#### Results

The results will be stored in the project destination's "crawler-documents"; in the File case:

    '/Users/pascal/sky_collections/testproj/crawler-documents/'

Each document will be stored with a slugified file name, with JSON content:

- Title "title"
- Main body "body"
- Publication date "publish_date"
- Domain "domain"
- Author "author"
- Images "images" (sorted on usefulness)
- Related links "related" (sorted on usefulness)
- Summary "summary"

### Scheduling

When using well defined crawling boundaries, recrawling can be done frequently, as it does not burden the target. 

Use this to update all the existing crawls:

    cs.run_all()

Use a cronjob to automate running a scheduling script, e.g. daily (perhaps more implementation is to follow).

### Next, Bad crawl/index settings

After crawling, it is recommended to check the summary of potential bad paths. For `title`, `body`, `publish_date`, and `url` the shortest (five) values are sorted so it can give a suggestion about which paths might be bad. (reasoning: if a title is really short or non existent, most likely it is a document that should be filtered)

```python
ccp = CrawlFilePlugin(plugin_name)
ccp.get_bad_documents()
```

To be extended.

### Glossary

- Backend
- Config
- Service
- Plugin

### Contribute

It is very much appreciated if you'd like to contribute in one or more of the following areas:

- More Backends
- Documentations/tests
- Improvement of detection
- NLP
