# Product Name
> Download data, HTML pages and whatever you like from static URLs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Whether you need to download a huge data dump or hundreds of HTML pages to analyze them locally, this tool might 
be the way to go. You will need a fairly static URL, where just an index counts up for every new file.

![download icon](download-icon.svg)

## Installation Examples

OS X & Linux:

```sh
# clone the project and install requirements into a virtual environment
git clone https://github.com/RichStone/data-collection-download-tool.git
cd data-collection-download-tool
python3 -m venv venv
pip3 install --upgrade setuptools pip
source venv/bin/activate
pip3 install -r requirements.txt
```

Windows(not tested yet):

```sh
# clone the project and install requirements into a virtual environment
git clone https://github.com/RichStone/data-collection-download-tool.git
cd data-collection-download-tool
python3 -m venv venv
pip3 install --upgrade setuptools pip
# you will probably need to make the "source" command available iny our cmd (e.g. by using Powershell/GitBash instead of cmd)
source venv/Scripts/activate
pip3 install -r requirements.txt
```

## Usage Examples

This will download every xkcd HTML page from `https://xkcd.com/1` to `https://xkcd.com/2000`:

```
python3 download.py https://xkcd.com/++1**2000++
```

You just need to connect the dynamic part of your URL by starting `++` and ending `++`. In between you must define a 
download range using integers and delimiting them by `**`

In more detail:

#### Get HTML pages

*(note: I took xkcd just a simple example to make clear how the tool works. If you want all xkcd images scraped from the 
website, you would rather use a library like BeautifulSoup to get them on the fly.)*

URLs, where the pictures are located:
```sh
https://xkcd/1
https://xkcd/2
https://xkcd/3
and so on ...
```
Say you want all HTML pages from 15 to 2100:
```sh
# run from the tools source directory
python3 download.py https://xkcd.com/++15**2100++
```
#### Get a Big Data Dump
The tool can also handle preceding zeros. E.g. to get the complete dump of pubmed, you would do this:
```sh
python3 download.py https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed18n++0001**0928++.xml.gz
```
## Development Setup
(in case you want to contribute to the download tool)

Installation is the same as described in "Installation Examples" above.

Python's unittest module is used for the tests. To run the tests from the commandline:
```sh
export PYTHONPATH=/your/path/to/data-collection-download-tool/
python3 tests/test_data_collection_tool.py
```

## Release History

* 0.0.1
    * First release to download from a static up counting URL

## Meta

Richard Steinmetz - [@LinkedIn](https://www.linkedin.com/in/richard-steinmetz/)  – [@Twitter](https://twitter.com/stonerichio)

Distributed under MIT license. See ``LICENSE.txt`` for more information.

[http://datagoodie.com](http://datagoodie.com)

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

Of course it would be great to keep the tool test-driven ;)

## Possible Future Features
- get really dynamic URLs
- exclude some ranges/files from download
- custom file naming/endings
- unzip option
- adding headers and sleep option for sensitive URLs
- GUI 🌈

Just let me know what you need for your use case or help me refining this tool.

## Necessary Code Refactoring
- factor parsing elements out of downloader.py
- solve wildcard dependency between Parser und Downloader elegantly