"""
This script downloads all available books written by P. O. Hviezdoslav (except for "1869 II." which must be downloaded manually)
from Zlatý fond SME (https://zlatyfond.sme.sk/autor/56/Pavol-Orszagh-Hviezdoslav).
"""

import os
import shutil
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

# Constants
ROOT_URL = "https://zlatyfond.sme.sk"
INDEX_URL = ROOT_URL + "/autor/56/Pavol-Orszagh-Hviezdoslav"
DOWNLOAD_URL = ROOT_URL + "/download/html"
DOWNLOAD_DIR = "books_html"
MANUALLY_DOWNLOADED_BOOKS = ["/dielo/1700/Orszagh-Hviezdoslav_1869-II"]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def main():
    """
    Main function that downloads all available books written by P. O. Hviezdoslav.
    """
    # Remove the existing download directory and create a new one
    shutil.rmtree(DOWNLOAD_DIR, ignore_errors=True)
    os.makedirs(DOWNLOAD_DIR)

    # Ge the list of book links
    book_links = get_book_links()
    print("Available books:")
    for i, book_link in enumerate(book_links):
        print(f"{(i + 1):2d}. {book_link}")
        if book_link in MANUALLY_DOWNLOADED_BOOKS:
            print("Excluded book. Skipping...")
            continue

        # Download the book HTML
        book_html_filename, book_html = get_book_html(book_link)
        if book_html is None or book_html_filename is None:
            print("Failed to download the book HTML. Skipping...")
            continue

        # Save the book HTML to a file
        book_html_path = os.path.join(DOWNLOAD_DIR, book_html_filename)
        with open(book_html_path, "w") as f:
            f.write(book_html)


def get_book_links():
    """
    Get the list of book links from the index page.
    """
    index_html = requests.get(INDEX_URL).text
    index_soup = BeautifulSoup(index_html, "html.parser")
    books_list_column = index_soup.find(attrs={"id": "tu-budu-knihy"})
    book_links = [a["href"] for a in books_list_column.find_all("a", href=True)]
    return book_links


def get_book_html(book_link):
    """
    Download the HTML content of a book.
    """
    book_url = ROOT_URL + book_link

    s = requests.Session()

    # Get the cookies
    s.get(book_url, headers=HEADERS)

    # Download the file using the same session
    response = s.get(DOWNLOAD_URL, headers=HEADERS)

    # Ensure the request was successful
    response.raise_for_status()

    # Get the filename from the Content-Disposition header, if it exists
    content_disposition = response.headers.get("content-disposition")
    if not content_disposition or "filename=" not in content_disposition:
        return None, None

    book_html_filename = unquote(content_disposition.split("filename=")[1])
    book_html = response.text

    return book_html_filename, book_html


if __name__ == "__main__":
    main()
