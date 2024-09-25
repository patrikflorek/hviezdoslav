![Hviezdoslav](hviezdoslav.jpg)


# P. O. Hviezdoslav's works

This repository contains collection of most of the poetic works of Slovak poet [Pavol Orszagh Hviezdoslav](https://en.wikipedia.org/wiki/Pavol_Orsz%C3%A1gh_Hviezdoslav). The purpose of this collection is to fine-tune a language model to generate poetry in style of P. O. Hviezdoslav.


## Dataset building

The dataset was built in several steps:

### HTML dataset

The data were initially downloaded from [Zlaty fond SME](https://zlatyfond.sme.sk/autor/56/Pavol-Orszagh-Hviezdoslav) using the script `download_html.py` and stored in the `./books_html` folder, where each file represents one book. The book "1869 II." cannot be downloaded programmatically and must be downloaded manually.
