import os
from pathlib import PurePosixPath
from sanitize_filename import sanitize
from urllib.parse import unquote, urlparse


def url_to_foldername(url):
    """
    Chomikuj url

    Input:
    url_to_foldername("https://chomikuj.pl/biblioholik/test/za*c5*bc*c3*b3*c5*82*c4*87+g*c4*99*c5*9bl*c4*85+ja*c5*ba*c5*84+ZA*c5*bb*c3*93*c5*81*c4*86+G*c4*98*c5*9aL*c4*84+JA*c5*b9*c5*83")

    Output:
    encoded: "za*c5*bc*c3*b3*c5*82*c4*87+g*c4*99*c5*9bl*c4*85+ja*c5*ba*c5*84+ZA*c5*bb*c3*93*c5*81*c4*86+G*c4*98*c5*9aL*c4*84+JA*c5*b9*c5*83"
    decoded -> "zażółć gęślą jaźń ZAŻÓŁĆ GĘŚLĄ JAŹŃ"

    TODO: annotate parts and return path relative to username
    """
    parts = PurePosixPath(
        unquote(
            urlparse(
                url
            ).path
        )
    ).parts
    folder = parts[-1]
    return folder

def decode_foldername(folder_name):
    """
    Decode foldername to utf-8
    """
    cnum = 0
    out = ''
    while cnum < len(folder_name):
        if folder_name[cnum]=='+': out += '%02x' % ord(' ')
        elif folder_name[cnum]==':': out += '%02x' % ord('-')
        elif folder_name[cnum]=='?': out += '%02x' % ord('_')
        elif folder_name[cnum]=='*':
            out += folder_name[cnum+1:cnum+3]
            cnum+=2
        else: out += '%02x' % ord(folder_name[cnum])
        cnum+=1
    return bytes.fromhex(out).decode('utf8')

def get_dest_path(url):

    enc_foldername = url_to_foldername(url)
    folder_name = decode_foldername(enc_foldername)    
    sanitized_folder = sanitize(folder_name)

    dest_path = os.path.join(os.getcwd(), 'downloads', sanitized_folder)

    return dest_path
    
def prepare_dest_folder(dest_path):
    """
    Prepare destination folder for download
    """

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
        print(f"Created folder: {dest_path}")
    
    print(f"Destination folder {dest_path} already exists.")
    return
