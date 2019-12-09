
import arxiv
import regex as re
from modules import regex_markers
import os

__author__ = "Gwena Cunha"

MAX_RES = 10000


def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def check_for_str(text, pattern):
    """ Checks for pattern in text

    :param text: string to check for pattern in
    :param pattern: pattern to check for
    :return: boolean confirming or denying the presence of pattern in string
    """
    has_url = False
    urls = re.findall(pattern, text)
    if len(urls) != 0:
        has_url = True
    return has_url


def check_for_url(text):
    """ Checks for URL in text

    :param text: string to check for URL in
    :return: boolean confirming or denying the presence of URL in string
    """
    try:
        return check_for_str(re.escape(regex_markers.WEB_URL_REGEX), text)
    except:
        print(text)
        print("Error")
        return True


def delete_line_breaks(text, joiner):
    """ Deletes line breaks and joins split strings in one line

    :param text: string
    :param joiner: string used to join items [" " for abs or "" for title]
    :return: joined text
    """
    text = text.split('\n')
    text = joiner.join(text)
    return text


def make_dataset_in_query(search_query, max_results, min_num_words=0, results_dir='results/'):
    """ Checks if max_result is bigger than MAX_RES

        Problem when max_results is too big (bigger than 10000)
        Solution: paging with start parameter
        30,000 is too big, but batches of 0-10,000 10,000-20,000 20,000-30,000 is not

    :param search_query: query articles in area of study
    :param max_results: max total number of articles
    :param min_num_words: filter for minimum number an abstract should have
    :return:
    """

    # Create results directory if not existent
    ensure_dir(results_dir)

    # Paging
    times_to_run = 0
    last_run = 0
    if max_results > MAX_RES:
        times_to_run, last_run = divmod(max_results, MAX_RES)

    start_idx = 0
    filename_title_array = []
    filename_abs_array = []
    total_num_articles = 0
    for i in range(times_to_run+1):
        start_idx = MAX_RES * i
        print("start_idx: {}".format(start_idx))
        max_paging = min(MAX_RES * (i+1), max_results) - start_idx
        print("max paging: {}".format(max_paging))
        filename_title_array_tmp, filename_abs_array_tmp, num_articles = \
            make_dataset(search_query, max_paging, max_results, min_num_words=min_num_words, start=start_idx,
                         results_dir=results_dir)
        filename_title_array.append(filename_title_array_tmp)
        filename_abs_array.append(filename_abs_array_tmp)
        total_num_articles += num_articles

    new_filename = results_dir + '{search_query}_{total_num_articles}_{final_max}_{min_num_words}'.format(
        search_query=search_query, total_num_articles=total_num_articles, final_max=max_results,
        min_num_words=min_num_words)

    # Joins pages in 1 file and delete temporary files
    join_pages(filename_title_array, filename_abs_array, new_filename)


def join_pages(filename_title_array, filename_abs_array, new_filename):
    """ Joins pages in 1 file and delete temporary files

    :param filename_title_array: array with title filenames obtaining from paging
    :param filename_abs_array: array with abs filenames obtaining from paging
    :param new_filename: New filename in the format results_dir/<search_query>_<total_num_articles>_<final_max>_<min_num_words>
    :return:
    """

    filename_title = new_filename+'_title.txt'
    filename_abs = new_filename + '_abs.txt'
    file_title = open(filename_title, 'w')
    file_abs = open(filename_abs, 'w')

    for t, a in zip(filename_title_array, filename_abs_array):
        file_title_tmp = open(t, 'r')
        title_tmp = file_title_tmp.read()
        file_abs_tmp = open(a, 'r')
        abs_tmp = file_abs_tmp.read()

        file_title.write(title_tmp)
        file_abs.write(abs_tmp)

        file_title_tmp.close()
        file_abs_tmp.close()
        os.remove(t)
        os.remove(a)

    file_title.close()
    file_abs.close()


def make_dataset(search_query, max_paging, max_results, min_num_words=0, start=0, results_dir='results/'):
    """ Makes dataset in query

    :param search_query: query articles in area of study
    :param max_paging: max number of articles per paging
    :param max_results: max total number of articles
    :param min_num_words: filter for minimum number an abstract should have
    :param start: start index
    :return: 2 strings (title and abstract filenames)
             1 int (num of articles)
    """
    # Keyword search
    articles = arxiv.query(query=search_query, max_results=max_paging, start=start)

    str_title = ''
    str_abs = ''
    for art in articles:

        # Delete line breaks and join them in one line
        str_title_tmp = delete_line_breaks(art.title, "")
        str_abs_tmp = delete_line_breaks(art.summary, " ")

        # Check for URL
        title_has_url = check_for_url(str_title_tmp)
        abs_has_url = check_for_url(str_abs_tmp)

        # Check for presence of "Proceedings of the"
        title_has_pattern = check_for_str(str_title_tmp, "Proceedings of the")
        abs_has_pattern = check_for_str(str_abs_tmp, "Proceedings of the")

        # Check min number of words
        word_count = len(str_abs_tmp.split())

        # Save title-abs combination in var
        if not (title_has_url or abs_has_url or title_has_pattern or abs_has_pattern) and word_count >= min_num_words:
            str_title += str_title_tmp + '\n'
            str_abs += str_abs_tmp + '\n'

    num_articles = len(str_title.split('\n')) - 1
    filename_title = results_dir + '{search_query}_{start}_{max_paging}_{num_articles}_{final_max}_{min_num_words}' \
                                   '_title.txt'.format(search_query=search_query, start=start, max_paging=max_paging,
                                                       num_articles=num_articles, final_max=max_results,
                                                       min_num_words=min_num_words)
    filename_abs = results_dir + '{search_query}_{start}_{max_paging}_{num_articles}_{final_max}_{min_num_words}' \
                                 '_abs.txt'.format(search_query=search_query, start=start, max_paging=max_paging,
                                                   num_articles=num_articles, final_max=max_results,
                                                   min_num_words=min_num_words)
    file_title = open(filename_title, 'w')
    file_abs = open(filename_abs, 'w')

    # Save information in file
    file_title.write(str_title)
    file_abs.write(str_abs)

    # Close files
    file_title.close()
    file_abs.close()

    return filename_title, filename_abs, num_articles


def make_dataset_in_group_of_queries(search_queries, max_results, min_num_words=0, results_dir='results/'):
    """ Makes dataset in a group of queries

    :param search_queries: list of search_query, format: {"query1", "query2"}
    :param max_results: max number of articles
    :param min_num_words: filter for minimum number an abstract should have
    :param start: start index
    :return:
    """

    for search_query in search_queries:
        make_dataset_in_query(search_query, max_results, min_num_words, results_dir=results_dir)


if __name__ == '__main__':

    results_dir = '../results/'

    # Make dataset in single query/area
    search_query = "artificial intelligence"
    max_results = 15000
    min_num_words = 200
    make_dataset_in_query(search_query, max_results, min_num_words=min_num_words, results_dir=results_dir)

    # Group of queries
    #search_queries = {"computer vision", "language generation"}
    #max_results = 15000
    #min_num_words = 15
    #make_dataset_in_group_of_queries(search_queries, max_results, min_num_words=min_num_words, results_dir=results_dir)

