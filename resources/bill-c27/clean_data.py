"""This script cleans the data scraped from the hansard site containing major speeches from the bill c-27 debate.
It saves the data in json file in the format:
[
    {
        "name": "name of the speaker",
        "party": "party of the speaker",
        "speech": "speech of the speaker",
        "url": "url of the speech"
    },
    ...
]

The topic we are looking for come after <h3 class="hansard3> containing the text "Digital Charter Implementation Act, 2022".
To create the correct bound you just need to find the next tag that is <h3> or higher.
"""
#%%
from parsel import Selector
from pathlib import Path
import json
import pandas as pd
import spacy

DATA_DIR = Path(__file__).parent / "data"
HTML_FILES = list(DATA_DIR.glob("*.html"))
TEXT = "Digital Charter Implementation Act, 2022"

#%%
def load_raw_html_from_file(filename: Path):
    """Loads the raw html from a file"""
    return filename.read_text()


# %%
html = load_raw_html_from_file(HTML_FILES[0])
sel = Selector(html)
header = sel.xpath(f"//h3[text()='{TEXT}']")
# %%
