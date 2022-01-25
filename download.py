
from bs4 import BeautifulSoup
import re
import requests
from utils import get_dest_path, prepare_dest_folder

def get_page_count(url):
    """
    Get number of pages in folder
    """
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    paginator = soup.select('#FilesListContainer > #listView > div.paginator')
    if len(paginator) == 0:
        return 1
    else:
        pages = paginator[0].select('a')
        return len(pages)

def download_mp3(url, dest_dir, filename):
    
    audio = requests.get(url)
    with open(f'{dest_dir}/{filename}.mp3', 'wb') as f:
        print(f"Downloading {filename}")
        f.write(audio.content)

def download_mp3_from_page(folder_url, dest_path):

    html = requests.get(folder_url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    links = soup.select('h3 > a')
    print(f"Found {len(links)} links")

    for link in links:
        if 'mp3' in link.get('href'):          
            m = re.match(r"^.*/(?P<name>.+),(?P<id>.+)\.(?P<ext>.+)\(audio\)$", link.get('href'))
            info = m.groupdict()
            download_url = f"http://chomikuj.pl/Audio.ashx?id={info['id']}&type=2&tp=mp3"

            download_mp3(download_url, dest_path, link.get('title'))

def download_folder(folder_url):
    
    # prepare destination folder if it doesn't exist
    dest_path = get_dest_path(folder_url)
    prepare_dest_folder(dest_path)

    pages = get_page_count(folder_url)
    print(f"Found {pages} pages")

    # download first page
    download_mp3_from_page(folder_url, dest_path)

    if pages > 1:
        # download other pages
        for page in range(2, pages+1):
            following_page_url = f"{folder_url},{page}"
            download_mp3_from_page(following_page_url, dest_path)



