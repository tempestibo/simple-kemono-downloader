import os
import requests
from bs4 import BeautifulSoup

# Header to pull requests from website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}

intro = r"""
  _  __                                                   
 | |/ /___ _ __ ___   ___  _ __   ___                     
 | ' // _ \ '_ ` _ \ / _ \| '_ \ / _ \                    
 | . \  __/ | | | | | (_) | | | | (_) |                   
 |_|\_\___|_| |_| |_|\___/|_| |_|\___/        _           
 |  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __ 
 | | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
 | |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
 |____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
                                                          
Welcome to my Kemono.su Image Downloader!
This is a very basic tool that currently supports only image downloads.
More functionality to come soon!
"""

print(intro)

# Kemono.su post URL
url = input("Input Post URL: ")
# url = "https://kemono.su/patreon/user/53912142/post/109647846"

# Folder path where images will be downloaded
folder_path = input("Input folder path (e.g., downloads/kemono_images): ")

# Ensure the folder exists, create it if it doesn't
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Makes a request to the post URL
r = requests.get(url=url, headers=headers)

# Parse through the html of the post URL
soup = BeautifulSoup(r.content, "html.parser")

# Finds all images from the post
figures = soup.find_all('figure')

# Converts html data to string
figures_str = str(figures)

# Converts previous string data to a list split by lines
figures_splitline = figures_str.splitlines()

# Separates actual high res image links from other data in the list
downloadable_img = [item for item in figures_splitline if item.startswith('<a class="fileThumb"')]

# Formats image link and downloads each image link in the downloadable_img list
for img in downloadable_img:
    hres = img.split('href="')[-1].strip('">')
    
    file_name = hres.split('f=')[-1]
    
    # Full path for saving the image in the folder
    image_path = os.path.join(folder_path, file_name)
    
    final_img = requests.get(hres, headers=headers)
    if final_img.status_code != 200:
        print(f'Error getting {file_name}')
    else:
        with open(image_path, 'wb') as f:
            f.write(final_img.content)
            print(f"Successfully downloaded {file_name} to {folder_path}")

print(f'Downloaded {len(downloadable_img)} files.')

input("Press Enter to Exit.")
