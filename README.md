## About

* Extract Abstract and Title Dataset from arXiv articles
* Domain of articles: search_query (i.e. Artificial Intelligence), case insensitive
* Exclude articles that have URL or "Proceeding of the" in the Title or Abstract
* Results filename format: <query>_<numner of articles>_<max number of articles>_<minimum number of words in abstract>

## Code
* Required to detect URLs and patterns
  ```
  pip install regex

  from regex import re
  ```

## Credits
[lukasschwab's Python wrapper](https://github.com/lukasschwab/arxiv.py) for the [arXiv API](http://arxiv.org/help/api/index)
  ```
  pip install arxiv
  ```
