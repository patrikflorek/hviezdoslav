"""
This script converts and reformat the downloaded books in HTML format to plain text format.
"""

import os
import re
import shutil
from bs4 import BeautifulSoup


HTML_DIR = "books_html"
TXT_DIR = "books_txt"


def main():
    """
    Main function to convert HTML books to plain text format.
    """
    # Remove the existing text directory and create a new one
    shutil.rmtree(TXT_DIR, ignore_errors=True)
    os.makedirs(TXT_DIR)

    print("Converting books from HTML to TXT format:")
    html_book_filenames = os.listdir(HTML_DIR)
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

        book_txt_dir = os.path.join(TXT_DIR, clean_book_title)
        os.makedirs(book_txt_dir, exist_ok=True)

        print("Chapters:")
        chapter_elements = book_element.find_all("div", attrs={"class": "chapter"})
        for i, chapter_element in enumerate(chapter_elements):
            chapter_title = (
                chapter_element.find(attrs={"class": "titlepage"})
                .find(attrs={"class": "title"})
                .get_text(strip=True)
            )
            clean_chapter_title = clean_text(chapter_title)
            print(f"  {i + 1:3d}. {clean_chapter_title}")

            # Remove references
            reference_elements = chapter_element.find_all("sup")
            for reference_element in reference_elements:
                reference_element.decompose()

            # Remove footnotes
            footnote_elements = chapter_element.find_all(attrs={"class": "footnotes"})
            for footnote_element in footnote_elements:
                footnote_element.decompose()

            # Combine all literal elements into one text
            literal_elements = chapter_element.find_all(
                attrs={"class": "literallayout"}
            )
            literal_texts = [
                literal_element.get_text(strip=False)
                for literal_element in literal_elements
            ]
            literal_text = "\n\n".join(literal_texts)
            clean_literal_text = clean_text(literal_text)

            reformatted_literal_text = reformat_text(clean_literal_text)

            txt_chapter_filename = f"{(i + 1):03} - {clean_chapter_title}.txt"
            txt_chapter_path = os.path.join(book_txt_dir, txt_chapter_filename)
            with open(txt_chapter_path, "wt") as f:
                f.write(f"{clean_chapter_title}\n\n\n{reformatted_literal_text}")


def clean_text(text):
    """
    Clean the text by removing unwanted characters and formatting.
    """
    # Remove non-breaking spaces
    text = text.replace("\u00A0", " ")
    # Replace ellipsis with three dots
    text = re.sub(r"…", r"...", text)
    # Replace single quotes
    text = re.sub(r"[‘’‚]", r"'", text)
    # Replace double quotes
    text = re.sub(r"[“„]", r'"', text)
    # Replace hyphens
    text = re.sub(r"—", r"-", text)
    # Replace accent
    text = re.sub(r"´", r"'", text)
    # Add space after punctuations if there is no other punctuation or quotes
    text = re.sub(r"""([!,.:;?])([^'".!?])""", r"\g<1> \g<2>", text)
    # Remove spaces before punctuations
    text = re.sub(r"""\s+([!,.:;?])""", r"\g<1>", text)
    # Replace multiple spaces with a single space
    text = re.sub(r" +", r" ", text)

    # Remove leading and trailing whitespace from lines
    lines = text.split("\n")
    lines = [line.strip() for line in lines]
    text = "\n".join(lines)

    return text


def reformat_text(text):
    """
    Reformat the text by removing empty lines and trimming whitespace.
    """
    # Split the text into lines and remove leading/trailing whitespace
    lines = [line.strip() for line in text.split("\n")]

    # Replace multiple empty lines with a single empty line
    i = 0
    while i < len(lines):
        if lines[i] == "" and (i == 0 or lines[i - 1] == ""):
            lines.pop(i)
        else:
            i += 1

    # Remove leading and trailing empty lines
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


if __name__ == "__main__":
    main()
