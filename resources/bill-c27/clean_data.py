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
from collections.abc import Iterable
from functools import partial
from typing import List

from bs4 import BeautifulSoup
from pathlib import Path
import json
from funcy import flatten, complement, takewhile
import pandas as pd
import spacy

DATA_DIR = Path(__file__).parent / "data"
HTML_FILES = list(DATA_DIR.glob("*.html"))
TEXT = "Digital Charter Implementation Act, 2022"

#%%
def load_raw_html_from_file(filename: Path):
    """Loads the raw html from a file"""
    return filename.read_text()

def get_soup(html: str):
    """Creates a soup from the html"""
    return BeautifulSoup(html, "lxml")

def find_all_header_tags(soup: BeautifulSoup):
    """Finds all the header tags in the soup"""
    return soup.find_all(["h1", "h2", "h3"])

def find_bill_sections(headers: list, header_text: str = TEXT):
    """Finds the bill sections in the headers"""
    return [header for header in headers if header_text in header.text]


def tag_not_header(tag: BeautifulSoup):
    """Returns True if the tag is not a header tag"""
    return tag.name not in ["h1", "h2", "h3"]


def tag_not_person_speaker(tag: BeautifulSoup):
    """Returns True if the tag is not a person speaker"""
    return "PersonSpeakingPopup" not in tag.attrs.get("class", [])


def get_all_tags_between_headers(section_tags: List[BeautifulSoup]):
    """Gets all the tags between the headers"""
    next_siblings = map(lambda x: x.nextSiblingGenerator(), section_tags)
    takewhile_not_header = partial(takewhile, tag_not_header)
    return [div for sibling in next_siblings for div in takewhile_not_header(sibling)]


def find_all_speakers(tag: BeautifulSoup):
    """Finds all the speakers in the tag"""
    return tag.find_all("div", class_="personSpeaking")


def get_text_of_tag(tag: BeautifulSoup):
    """Gets the text of a tag"""
    return " ".join(tag.stripped_strings)


def get_speaker_name(speaker: BeautifulSoup):
    """Gets the name of a speaker from the speaker tag"""
    return " ".join(speaker.strings).strip()

def get_speakers_speech(speaker: BeautifulSoup):
    """Gets the speech of a speaker
    
    The speaker tag is below a 'paratext' span. All siblings of the span are the speech.
    """
    parent_span = speaker.findParent("span")
    # TODO: remove the speaker name from the beginning of the speech, ideally by taking the <a> tag out of the parent span
    parent_span_without_speaker_name = parent_span.find("a").extract()
    all_tags = [parent_span] + list(parent_span.nextSiblingGenerator())
    return " ".join(s.strip() for tag in all_tags for s in tag.strings)

def list_of_speakers_with_speeches(speech_tags: List[BeautifulSoup]):
    """Gets a list of speakers with their speeches"""
    return [[get_speaker_name(speaker), get_speakers_speech(speaker)] for speaker in find_all_speakers(s)]

# %%
html = load_raw_html_from_file(HTML_FILES[0])
soup = BeautifulSoup(html, "lxml")
headers = soup.find_all(["h1", "h2", "h3"])
bill_sections = [header for header in headers if TEXT in header.text]
speech_tags = get_all_tags_between_headers(bill_sections)
all_speeches = " ".join([get_text_of_tag(tag) for tag in speech_tags])
# %%

current_section = None
speeches = []
for tag in headers:
    if TEXT in tag.text:
        current_section = tag

#%%
sublists = [
    [1,2,[3,4,[5,6]]],
    [7,8,[9,10,[11,12]]]
]
result = flatten_arbitrary_list(sublists)
print(result)
# %%
