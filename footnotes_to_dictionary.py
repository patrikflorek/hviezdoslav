"""
This script combines footnotes extracted from HTML books and footnotes manually copied from the web into a single dictionary CSV file.
The dictionary rows contains the following columns: `term`, `definition`, `book`, `chapter`.
"""

import re
import pandas as pd


def main():
    """
    Main function to combine footnotes and create a dictionary CSV file.
    """
    # Load footnotes from CSV files
    footnotes_manual_download = pd.read_csv("FOOTNOTES_MANUAL_DOWNLOAD.csv")
    footnotes_extracted = pd.read_csv("footnotes_extracted.csv")

    # Combine footnotes into a single DataFrame
    footnotes = pd.concat([footnotes_manual_download, footnotes_extracted])
    footnotes = footnotes.sort_values(by=["book", "chapter", "footnote"])
    footnotes.to_csv("footnotes.csv", index=False)

    # Initialize an empty DataFrame for the dictionary
    dictionary = pd.DataFrame(columns=["term", "definition", "book", "chapter"])

    # Extract terms and definitions from footnotes
    for _, row in footnotes.iterrows():
        book = row["book"]
        chapter = row["chapter"]
        footnote = row["footnote"]
        term, definition = extract_term_and_definition(footnote)
        if not term:
            continue

        # Append the extracted term and definition to the dictionary
        dictionary = pd.concat(
            [
                dictionary,
                pd.DataFrame(
                    [[term, definition, book, chapter]], columns=dictionary.columns
                ),
            ],
            ignore_index=True,
        )

    # Sort the dictionary by term and save it to a CSV file
    dictionary = dictionary.sort_values(by="term")
    dictionary.to_csv("dictionary.csv", index=False)


def extract_term_and_definition(footnote):
    """
    Extract the term and definition from a footnote.

    Args:
        footnote (str): The footnote text.

    Returns:
        tuple: The extracted term and definition.
    """
    match = re.match(r"\[(\d+)\] (.+?) - (.+)", footnote)
    if match:
        term = match.group(2)
        definition = match.group(3)
        return term, definition
    else:
        return "", ""


if __name__ == "__main__":
    main()
