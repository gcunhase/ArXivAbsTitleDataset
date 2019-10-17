[![DOI](https://zenodo.org/badge/128865634.svg)](https://zenodo.org/badge/latestdoi/128865634)

## About
Extracts Abstract and Title Dataset from arXiv articles

#### Contents
[Requirements](#requirements) • [Code](#code) • [How to Cite](#acknowledgement)

## Requirements
* Required to detect URLs and patterns
  ```
  pip install regex arxiv

  from regex import re
  ```
  > `pip install arxiv`: [lukasschwab's Python wrapper](https://github.com/lukasschwab/arxiv.py) for the [arXiv API](http://arxiv.org/help/api/index)

## Code
* Domain of articles: search_query (i.e. Artificial Intelligence), case insensitive
* Exclude articles that have URL or "Proceeding of the" in the Title or Abstract
* Results filename format: ```<query>_<start index>_<max number of articles is paging>_<actual number of articles>_<total max number of articles>_<minimum number of words in abstract>```

## Acknowledgement
Please star or fork if this code was useful for you. If you use it in a paper, please cite as:
```
@misc{cunha_sergio2019arxiv_abstract2title,
    author       = {Gwenaelle Cunha Sergio},
    title        = {Extracting Abstract and Title Dataset from arXiv articles},
    month        = oct,
    year         = 2019,
    doi          = {10.5281/zenodo.3496527},
    version      = {v1.0},
    publisher    = {Zenodo},
    url          = {https://github.com/gcunhase/ArXivAbsTitleDataset}
    }
```
