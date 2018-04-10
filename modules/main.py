
import arxiv
import re
from modules import regex_markers
import os

__author__ = "Gwena Cunha"


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
    return check_for_str(regex_markers.WEB_URL_REGEX, text)


def delete_line_breaks(text, joiner):
    """ Deletes line breaks and joins split strings in one line

    :param text: string
    :param joiner: string used to join items [" " for abs or "" for title]
    :return: joined text
    """
    text = text.split('\n')
    text = joiner.join(text)
    return text


if __name__ == '__main__':

    # Keyword search
    search_query = "artificial intelligence"
    max_results = 100
    articles = arxiv.query(search_query=search_query, max_results=max_results)

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

        # Save title-abs combination in var
        if not (title_has_url or abs_has_url or title_has_pattern or abs_has_pattern):
            str_title += str_title_tmp + '\n'
            str_abs += str_abs_tmp + '\n'

    # Open text files
    results_dir = "results/"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    num_articles = len(str_title.split('\n')) - 1
    filename_title = results_dir + 'title_{search_query}_{num_articles}_{max_results}.txt'.\
        format(search_query=search_query, num_articles=num_articles, max_results=max_results)
    filename_abs = results_dir + 'abs_{search_query}_{num_articles}_{max_results}.txt'.\
        format(search_query=search_query, num_articles=num_articles, max_results=max_results)
    file_title = open(filename_title, 'w')
    file_abs = open(filename_abs, 'w')

    # Save information in file
    file_title.write(str_title)
    file_abs.write(str_abs)

    # Close files
    file_title.close()
    file_abs.close()
