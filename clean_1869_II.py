"""
This script cleans the texts (chapters/poems) of the "1869. II." book
and saves them in corresponding files in `books_txt` folder.
"""

import os
import shutil
from difflib import Differ
from html_to_text import clean_text, reformat_text

# Constants
SOURCE_DIR = "./BOOKS_MANUAL_DOWNLOAD_TXT/1869. (II.)"
TARGET_DIR = "./books_txt/1869. (II.)"

d = Differ()


def main():
    """
    Main function to clean and copy the book chapters/poems.
    """
    print("Cleaning and copying a book: ", SOURCE_DIR.split("/")[-1])
    chapter_filenames = sorted(os.listdir(SOURCE_DIR))

    # Remove the target directory and create a new one
    shutil.rmtree(TARGET_DIR, ignore_errors=True)
    os.makedirs(TARGET_DIR, exist_ok=True)

    print("Chapters:")
    for chapter_filename in chapter_filenames:
        print(f"  * {chapter_filename}")
        chapter_path = os.path.join(SOURCE_DIR, chapter_filename)
        with open(chapter_path, "rt") as f:
            chapter_text = f.read()

        # Clean and reformat the chapter name
        chapter_base_filename = chapter_filename.split(".")[0]
        chapter_filename_prefix = chapter_base_filename[:6]
        chapter_name = chapter_base_filename[6:]
        clean_chapter_name = clean_text(chapter_name).strip()
        clean_chapter_filename = f"{chapter_filename_prefix}{clean_chapter_name}.txt"
        if clean_chapter_filename != chapter_filename:
            print(
                f"    Filename changed: '{chapter_filename}' -> '{clean_chapter_filename}'"
            )

        # Clean and reformat the chapter text
        clean_chapter_text = clean_text(chapter_text)
        clean_chapter_text = reformat_text(clean_chapter_text)

        # Print difference if the text was modified during cleaning
        if clean_chapter_text != chapter_text:
            delta = list(
                d.compare(
                    chapter_text.splitlines(keepends=True),
                    clean_chapter_text.splitlines(keepends=True),
                )
            )
            for line in delta:
                if line[0] in "+-?":
                    print(" " * 7, line, end="")

        print()

        # Save the cleaned chapter text to a new file
        clean_chapter_path = os.path.join(TARGET_DIR, clean_chapter_filename)
        with open(clean_chapter_path, "wt") as f:
            f.write(f"{clean_chapter_name}\n\n\n{clean_chapter_text}")


if __name__ == "__main__":
    main()
