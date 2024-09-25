"""
This script extracts footnotes from the books in HTML format and saves them in a CSV file.
"""

import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from html_to_text import clean_text

# Constants
HTML_DIR = "books_html"
FOOTNOTES_PATH = "footnotes_extracted.csv"


def main():
    """
    Main function to extract footnotes from the HTML books and save them in a CSV file.
    """
    html_book_filenames = os.listdir(HTML_DIR)
    footnotes = []
    for html_book_filename in html_book_filenames:
        print(f"{html_book_filename}")
        html_book_path = os.path.join(HTML_DIR, html_book_filename)
        with open(html_book_path, "rt") as f:
            html_book = f.read()

        soup = BeautifulSoup(html_book, "html.parser")
        book_element = soup.body.find(attrs={"class": "book"})
        book_title = (
            book_element.find(attrs={"class": "titlepage"})
            .find(attrs={"class": "title"})
            .get_text(strip=True)
        )
        clean_book_title = clean_text(book_title)
        print(f"Title: {clean_book_title}")

        print("Chapters:")
        chapter_elements = book_element.find_all("div", attrs={"class": "chapter"})
        for chapter_element in chapter_elements:
            chapter_title = (
                chapter_element.find(attrs={"class": "titlepage"})
                .find(attrs={"class": "title"})
                .get_text(strip=True)
            )
            clean_chapter_title = clean_text(chapter_title)
            print(f"  {clean_chapter_title}")

            # Extract chapter footnotes
            footnote_elements = chapter_element.find_all(attrs={"class": "footnotes"})
            for footnote_element in footnote_elements:
                footnote_text = footnote_element.get_text(strip=False)
                clean_footnote_text = clean_text(footnote_text)
                chapter_element_footnotes = get_element_footnotes(clean_footnote_text)
                for footnote in chapter_element_footnotes:
                    record = (clean_book_title, clean_chapter_title, footnote)
                    footnotes.append(record)
        print()

    # Save the footnotes to a CSV file
    footnotes_df = pd.DataFrame(footnotes, columns=["book", "chapter", "footnote"])
    footnotes_df.to_csv(FOOTNOTES_PATH, index=False)


def get_element_footnotes(footnote_text):
    """
    Extract footnotes from the given text.

    Args:
        footnote_text (str): The text containing footnotes.

    Returns:
        list: The list of extracted footnotes.
    """
    # Get all substrings that starts with a number between square brackets and ends before the end or the next number between square brackets
    footnotes = re.findall(r"\[\d+\].*?(?=\[\d+\]|$)", footnote_text)
    return footnotes


if __name__ == "__main__":
    main()
