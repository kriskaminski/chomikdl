import argparse
from download import download_folder

parser = argparse.ArgumentParser()
parser.add_argument('url', help='Url to chomikuj folder with mp3 files')
args = parser.parse_args()

if __name__ == '__main__':
    if not args.url:
        print("Please provide url to folder")    
    
    download_folder(args.url)



