"""
Download the project datafiles from Google Drive.

    -> files will be saved in a new folder: "data".
"""

import gdown
from zipfile import ZipFile
import os


url = "https://drive.google.com/u/0/uc?id=1iuXLv3NpBLvxNpJwsYmLk4IX2TyjGtvP"

zipped_data = "data.zip"
gdown.download(url, zipped_data)
with ZipFile(zipped_data, 'r') as zip:
    zip.extractall("data/")
os.remove("data.zip")
