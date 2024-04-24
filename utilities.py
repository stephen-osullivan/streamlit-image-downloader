import requests

import concurrent.futures
import os
import time
from typing import List, Optional
import zipfile

def download_image(url: str, save_file: Optional[str] = None) -> bool:
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
        print(f"Failed to download {save_file}.")
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
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit the tasks to the executor
        threads = []
        for url, save_file in zip(urls, save_files):
            threads.append(executor.submit(download_image, url, save_file))
        results = []
        for f in concurrent.futures.as_completed(threads):
           results.append(f.result())
        return results
        
    print('Total Execution time:', time.time()-t0)


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


