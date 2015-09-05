### sky

sky is a web scraping framework, implemented with the latest python versions in mind (3.4+). It uses the asynchronous `asyncio` framework, as well as many popular modules and extensions.

Most importantly, it aims for **next generation** web crawling where machine intelligence is used to speed up the development/maintainance/reliability of crawling.

It mainly does this by considering the user to be interested in content from *domains*, not just a collection of *single pages*.

**See it live in action with a news website YOU propose**:

- Locally  ([view demo](#demo))!
- Remotely (needs hosting)

Similar data will be very easy to use in your own applications.

#### Features/Goals

These are the features/goals of `sky`. Checkmarks have been accomplished:

- ✓ **Really fast**, due to Python 3.4+ new asyncio/aiohttp libraries, based on [500lines/crawler](https://github.com/aosabook/500lines/tree/master/crawler)
- ✓ **Smart**, due to considering crawling of *websites* instead of single *pages*
- ✓ **Boilerplate FREE**, removes crappy content (images, text, etc) that does not belong on pages
- ✓ **Nice API**, carefully crafted, easily extendible
- ✓ **Open-source**, democracy driven, with actual support
- ✓ **Free**, versus enormous costs for even medium scale projects using (worse) online services
- **Link-graph-analysis**, find out how a domain "looks" like
- **Automatic Natural Language Processing**, there have been steps to automatically detect acquisitions (`Company A acquires Company B`) and investments: `Company A invests B millions in Company C`.

#### Templating approach

By considering crawl content to originate from a *domain*, rather than *individual pages*, the following willl be possible:

- ✓ Drop duplicate content (menus, texts, images)
- ✓ Provide error checking tools (making sure no bad documents slip by)
- Detect whether a website changed the layout (causing other scrapers to fail)
- Understand sections of a website, such as comments, forum posts, related links etc
- Consider which pages are linked to which (star graph)
- Figure out the content pages by just pointing at the domain
- Relate pages (page A is related by content to page B)
- Consider an optimal re-crawling path

#### Installation

Use pip to install sky:

```python
pip3 install -U sky
```

This will install only the required packages. Optional packages are for backends, such as elasticsearch, cloudant and ZODB. Storing data on the local system does not require any packages.

#### Demo

Run a demo locally:

- [Install](#installation) `sky`
- Run `sky view` at the command line
- Visit [localhost:7900](http://localhost:7900) (use `-port <PORT>` to change port).
- Enter a URL and see the results after clicking `>>>`.

Possibly tweak the crawl with a few parameters after clicking `>Options`

The demo uses a standard configuration that could easily be improved on when setting up a project.

<img src="https://github.com/kootenpv/sky/blob/master/resources/skyview.png" />

#### Using the package

To setup a project/crawling service, visit [this readme](https://github.com/kootenpv/sky/tree/master/sky/README.md) for a "Getting started".

#### Contribute

It is very much appreciated if you'd like to contribute in one or more of the following areas:

- More Backends
- Documentations/tests
- Improvement of detection
- NLP
