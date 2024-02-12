# Download HTML files of selected P.O.Hviezdoslav books from the Zlatý fond SME website

import os
import shutil

import requests

from bs4 import BeautifulSoup

# Download HTML files of selected P.O. Hviezdoslav books from the Zlatý fond SME website

ROOT_URL = "https://zlatyfond.sme.sk"
INDEX_URL = ROOT_URL + "/autor/56/Pavol-Orszagh-Hviezdoslav"

# Create afresh download directory
DOWNLOAD_DIR = "HTML"

if os.path.exists(DOWNLOAD_DIR):
    shutil.rmtree(DOWNLOAD_DIR)

os.mkdir(DOWNLOAD_DIR)

# Download list of available books
index_html = requests.get(INDEX_URL).text
index_soup = BeautifulSoup(index_html, "html.parser")
books_list_column = index_soup.find(attrs={"id": "tu-budu-knihy"})
available_books = [a["href"] for a in books_list_column.find_all("a", href=True)]

# Author's poems
SELECTED_BOOKS = [
    "/dielo/273/Orszagh-Hviezdoslav_Dozvuky-II",
    "/dielo/18/Hviezdoslav_Hajnikova-zena",
    "/dielo/132/Orszagh-Hviezdoslav_Basne-prilezitostne",
    "/dielo/220/Orszagh-Hviezdoslav_Gabor-Vlkolinsky",
    "/dielo/272/Orszagh-Hviezdoslav_Dozvuky-I",
    "/dielo/161/Orszagh-Hviezdoslav_Prechadzky-jarom",
    "/dielo/196/Orszagh-Hviezdoslav_Zalmy-a-hymny",
    "/dielo/112/Orszagh-Hviezdoslav_Krvave-sonety",
    "/dielo/146/Orszagh-Hviezdoslav_Ezo-Vlkolinsky",
    "/dielo/260/Orszagh-Hviezdoslav_Rachel",
    "/dielo/261/Orszagh-Hviezdoslav_Kain",
    "/dielo/274/Orszagh-Hviezdoslav_Dozvuky-III",
    "/dielo/1250/Orszagh-Hviezdoslav_1916-1920",
    "/dielo/31/Orszagh-Hviezdoslav_Stesky-3",
    "/dielo/28/Orszagh-Hviezdoslav_Stesky-2",
    "/dielo/27/Orszagh-Hviezdoslav_Stesky-1",
    "/dielo/509/Orszagh-Hviezdoslav_Agar",
    "/dielo/2059/Orszagh-Hviezdoslav_Na-obnocke",
    "/dielo/1170/Orszagh-Hviezdoslav_Kratsia-epika-historicka-a-spolocenska",
    "/dielo/1171/Orszagh-Hviezdoslav_Kratsia-epika-zo-zivota-dedinskeho-ludu",
    "/dielo/25/Orszagh-Hviezdoslav_V-pamat",
    "/dielo/11/Orszagh-Hviezdoslav_Letorosty-I",
    "/dielo/159/Orszagh-Hviezdoslav_Letorosty-II",
    "/dielo/202/Orszagh-Hviezdoslav_Letorosty-III",
    "/dielo/20/Orszagh-Hviezdoslav_Azyl",
    "/dielo/113/Orszagh-Hviezdoslav_Sonety",
    "/dielo/1172/Orszagh-Hviezdoslav_Butora-a-Cutora",
    "/dielo/1173/Orszagh-Hviezdoslav_Prvy-zaprah",
    "/dielo/1174/Orszagh-Hviezdoslav_Poludienok",
    "/dielo/1175/Orszagh-Hviezdoslav_Vecera",
    "/dielo/1176/Orszagh-Hviezdoslav_V-zatvu",
    "/dielo/179/Orszagh-Hviezdoslav_Prechadzky-letom",
    "/dielo/1697/Orszagh-Hviezdoslav_Basnicke-prviesenky-Jozefa-Zbranskeho",
    "/dielo/1700/Orszagh-Hviezdoslav_1869-II",
    "/dielo/1699/Orszagh-Hviezdoslav_1869-I",
    "/dielo/1698/Orszagh-Hviezdoslav_Z-basni-venovanych-A-Medzihradskemu",
    "/dielo/1696/Orszagh-Hviezdoslav_Stesky-4",
]

# Exclude author's non poetic works
EXCLUDED_BOOKS = [
    "/dielo/1143/Orszagh-Hviezdoslav_Herodes-a-Herodias",  # Doesn't work
    "/dielo/1701/Orszagh-Hviezdoslav_Vzhledanie",  # Doesn't work
    "/dielo/1821/Orszagh-Hviezdoslav_Korespondencia-P-O-Hviezdoslava-so-Svetozarom-Hurbanom-Vajanskym-a-Jozefom---------Skultetym",
]

print("Available books:")
for i, book_link in enumerate(available_books):

    if book_link in SELECTED_BOOKS:
        status = ""  # "[SELECTED]"
    elif book_link in EXCLUDED_BOOKS:
        status = "[EXCLUDED]"
    else:
        status = "[NEW]"

    print(f"{(i + 1):2d}. {book_link} {status}")

    # Download selected books
    if book_link in SELECTED_BOOKS:
        book_url = ROOT_URL + book_link
        book_html = requests.get(book_url).text
        book_html_filename = (
            book_link.split("/")[-1] + ".html"
        )  # Use last part of the book URI as filename
        book_html_path = os.path.join(DOWNLOAD_DIR, book_html_filename)
        with open(book_html_path, "w") as f:
            f.write(book_html)
