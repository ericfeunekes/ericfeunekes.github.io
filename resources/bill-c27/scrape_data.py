"""This script scrapes the speeches from the hansard site containing major speeches from the bill c-27 debate.
It saves the speeches in html format in the data directory.
"""
#%%
import httpx
from pathlib import Path

#%% 
URLS = [
    "https://www.ourcommons.ca/DocumentViewer/en/44-1/house/sitting-125/hansard",
    "https://www.ourcommons.ca/DocumentViewer/en/44-1/house/sitting-136/hansard",
]
#%%
DATA_DIR = Path(__file__).parent / "data"

#%%
def extract_raw_html(url):
    """Extracts the raw html from the url"""
    response = httpx.get(url)
    return response.text

def save_raw_html_to_file(html, filename: Path):
    """Saves the raw html to a file"""
    if not filename.parent.exists():
        filename.parent.mkdir(parents=True)
    filename.write_text(html)

def get_data_dir():
    """Returns the data directory"""
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)
    return DATA_DIR

def main(data_dir: Path = DATA_DIR):
    """Main function"""
    for url in URLS:
        html = extract_raw_html(url)
        filename = data_dir / f"{url.split('/')[-2]}.html"
        save_raw_html_to_file(html, filename)

if __name__ == "__main__":
    data_dir = get_data_dir()
    main(data_dir=data_dir)