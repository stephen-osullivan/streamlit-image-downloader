from duckduckgo_search import DDGS
from PIL import Image
import requests

import concurrent.futures
import glob
import os
import shutil
import time
from typing import List, Optional
import zipfile

def download_image(url: str, save_file: Optional[str] = None) -> bool:
  """
  downloads a single image from a url and saves it
  """
  try:
    response = requests.get(url)
    if save_file is None:
        save_file = url.split('/')[-1]
    # Check if the request was successful
    if response.status_code == 200:
        # Open a new file in binary mode and write the image data
        with open(save_file, "wb") as file:
            file.write(response.content)
            print(save_file, "downloaded successfully!")
        return url, save_file, True
    else:
        print(f"Failed to download {save_file} (non 200 response).")
        return url, save_file, False
  except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return url, save_file, False
     
def download_images(
    urls: List[str], 
    save_files: Optional[List[str]] = None, 
    save_folder: Optional[str] = None) -> None:
    """
    use multi threading to download images
    """
    t0 = time.time()
    if save_files is None:
       save_files = [url.split('/')[-1] for url in urls]
    if save_folder:
        os.makedirs(save_folder, exist_ok=True)
        save_files = [f'{save_folder}/{save_file}' for save_file in save_files]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        # Submit the tasks to the executor
        threads = []
        for url, save_file in zip(urls, save_files):
            threads.append(executor.submit(download_image, url, save_file))
        results = []
        for f in concurrent.futures.as_completed(threads):
           results.append(f.result())
        return results
        
    print('Total Execution time:', time.time()-t0)

def delete_corrupted_images(folder:str):
    for file in find_images(folder):
        try:
            Image.open(file)
        except Exception as e:
            os.remove(file)
            print(f'Removed {file} due to following exception:\n {e}')

def ddg_download(query, num_images:int = 10, folder: str = 'downloads'):
    """
    download using duckduckgo
    """
    search_results = DDGS().images(keywords=query, max_results=num_images, safesearch='off')

    image_urls = [r['image'] for r in search_results] 
    # filter on pngs, jpgs
    #image_urls = [r for r in image_urls if r.split('.')[-1] in ['jpg', 'png']]
    save_folder = os.path.join(folder,query.replace(" ", "-"))
    results = download_images(image_urls, save_folder = save_folder)
    delete_corrupted_images(save_folder)

def zip_files(zip_filename, file_paths):
    """
    Creates a ZIP archive containing the files specified by the file_paths.

    Args:
        zip_filename (str): The name of the ZIP file to create.
        file_paths (list): A list of file paths to include in the ZIP archive.
    
    Example usage:
        files_to_zip = ['file1.txt', 'file2.py', 'folder/file3.jpg']
        zip_files('archive.zip', files_to_zip)
    """
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for file_path in file_paths:
            zip_file.write(file_path)
    print('Created zip file:', zip_filename)

def find_images(folder: str):
    """
    find all images in a folder
    """
    # Example usage
    image_formats = ['jpg','png','webp']
    image_list = []
    for format in image_formats:
        image_list += glob.glob(f'{folder}/**/*.{format}*', recursive=True)
    return image_list

def delete_subfolders(directory: str ='downloads'):
    """
    Removes all subdirectories (but not the parent directory) in the specified directory.
    Args:
        directory (str): The path to the directory where subdirectories need to be removed.

    # Example usage
    remove_subdirectories("/path/to/parent/directory")
    """
    if directory == "":
        return False
    
    if not os.path.isdir(directory):
        print('Directory does not exist:', directory)
        return False

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Removed directory: {item_path}")
        elif os.path.isfile(item_path):
            os.remove(item_path)
            print(f"Removed file: {item_path}")
        else:
            continue
    return True

