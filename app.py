import streamlit as st
from utilities import *
from duckduckgo_search import DDGS
from utilities import *
# test download


st.title('Image Downloader')
search_query = st.text_input('What would you like to download pictures of?')
num_images = st.slider('How many images', 0, 100, 10)
download = st.button('Download')
if download:
    delete_subfolders('downloads')
    download_folder = search_query.replace(" ", "-")
    results = ddg_download(search_query, num_images)
    num_downloaded = sum([r[2] for r in results])

    st.write(f'Successfully download {num_downloaded} images. Sample downloaded images:')
    images = find_images(f'downloads/{download_folder}')[:3]
    st.image(images, use_column_width=True)