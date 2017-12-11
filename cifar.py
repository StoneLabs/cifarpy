###################################################
#
# Functions for downloading the CIFAR-10 dataset
#
###################################################

from clint.textui import progress

import numpy as np
import download
import requests
import tarfile
import hashlib
import shutil
import pickle
import glob
import os

# Configuration

_CIFAR_10_URL_ = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
_CIFAR_10_MD5_ = "c58f30108f718f92721af3b95e74349a"
_PATH_CPICKLE_ = "DATA/cifar-10-batches-py/"
_PATH_ARCHIVE_ = "DATA/archive.tar.gz"
_PATH_EXTRACT_ = "DATA/"

# Logic

def __cifar_prompt(question):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    prompt = " [Y/n] "

    while True:
        raw_inp = input(question + prompt)
        choice = raw_inp.lower()
        if choice == '':
            return True
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def __cifar_exists():
    if not os.path.isfile(_PATH_ARCHIVE_):
        return False
    file = open(_PATH_ARCHIVE_, 'rb')
    hash = hashlib.md5(file.read()).hexdigest()
    if hash == _CIFAR_10_MD5_:
        return True
    return hash

def __cifar_download():
    print("--> Downloading data...")
    request = requests.get(_CIFAR_10_URL_, stream=True)
    with open(_PATH_ARCHIVE_, 'wb') as f:
        total_length = int(request.headers.get('content-length'))
        for chunk in progress.bar(request.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()

def __cifar_extract():
    print("--> Extracting data...")
    if os.path.exists(_PATH_CPICKLE_):
        if not __cifar_prompt("Target folder exists already. Replace?"):
            return
        shutil.rmtree(_PATH_CPICKLE_)

    tar = tarfile.open(_PATH_ARCHIVE_, "r:gz")
    tar.extractall(path = _PATH_EXTRACT_)
    tar.close()

def __unpickle(file):
    print("Loading %s..." % file, end="")
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict
    print(" ok")

def __cifar_download():
    print("--> Loading CIFAR-10...")
    state = __cifar_exists()
    if state == True:
        print("File already present!")
        print("MD5-Hash matches: %s" % _CIFAR_10_MD5_)
    elif state == False:
        print("File not present!")
        __cifar_download()
    else:
        print("File already present!")
        print("MD5-Hash mismatch:\n\texpected:\t%s\n\tcalculated:\t%s" % (_CIFAR_10_MD5_, state))
        if __cifar_prompt("Replace file?"):
            __cifar_download()
    
    __cifar_extract()
    print("--> CIFAR-10 loaded sucessfully")

def cifar_load():
    if not os.path.exists(_PATH_CPICKLE_):
        raise Exception("Data not found. Run cifar.py as a script to download the data!")
    print(glob.glob(_PATH_CPICKLE_ + "data_batch_*"))

if __name__ == "__main__":
    __cifar_download()