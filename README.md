[![DOI](https://zenodo.org/badge/128865634.svg)](https://zenodo.org/badge/latestdoi/128865634)

## About
Extracts Abstract and Title Dataset from arXiv articles

### Contents
[Requirements](#requirements) • [Code](#code) • [How to Cite](#acknowledgement)

## Requirements
* Python 3.6
  ```
  pip install -r requirements.txt
  ```
  > `arxiv`: [lukasschwab's Python wrapper](https://github.com/lukasschwab/arxiv.py) for the [arXiv API](http://arxiv.org/help/api/index)

## Code
* Domain of articles: search_query (i.e. Artificial Intelligence), case insensitive
* Exclude articles that have URL or "Proceeding of the" in the Title or Abstract
* Results filename format:
    ```
    <QUERY>_<START_INDEX>_<MAX_NUMBER_ARTICLES_IN_PAGING>_<ACTUAL_NUMBER_ARTICLES>_<TOTAL_MAX_NUMBER_ARTICLES>_<MIN_NUMBER_WORDS_ABS>
    ```

## Acknowledgement
Please star or fork if this code was useful for you. If you use it in a paper, please cite as:
```
@software{cunha_sergio2019arxiv_abstract2title,
    author       = {Gwenaelle Cunha Sergio},
    title        = {{gcunhase/ArXivAbsTitleDataset: Extracting Abstract and Title Dataset from arXiv articles}},
    month        = oct,
    year         = 2019,
    doi          = {10.5281/zenodo.3496527},
    version      = {v1.0},
    publisher    = {Zenodo},
    url          = {https://github.com/gcunhase/ArXivAbsTitleDataset}
    }
```
