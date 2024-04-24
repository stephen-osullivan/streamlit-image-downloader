import streamlit as st
from utilities import *
from duckduckgo_search import DDGS
from utilities import *

st.title('📸 Image Downloader')
st.write("""
         Put in a search query on the sidebar. The app will get the selected number of images.
         \nYou can then display a sample before downloading into a zip file.""")
# side bar
search_query = st.sidebar.text_input('What would you like to download pictures of?')
num_images = st.sidebar.slider('How many images', 0, 100, 10)
download = st.sidebar.button('Get Images')    

if download:
    delete_subfolders('downloads')
    download_folder = search_query.replace(" ", "-")
    results = ddg_download(search_query, num_images)

images_downloaded = find_images('downloads')
num_downloaded = len(images_downloaded)

if num_downloaded > 0:
    st.write(f'**Successfully download {num_downloaded} images. View a sample:**')
    num_display = st.slider('Images to Display', min_value =1, max_value=num_downloaded, value=1)
    st.image(
        images_downloaded[:num_display], use_column_width=True, caption=images_downloaded[:num_display])


# allow the user to extract a zip file containing the images.
zip_and_download = st.sidebar.button('Zip and Download')
if zip_and_download:
    download_folder = search_query.replace(" ", "-")
    download_path = os.path.join('downloads', download_folder)
    zip_path = download_path + '.zip' 
    zip_files(zip_path, find_images(download_path))
    with open(zip_path, "rb") as f:
        st.sidebar.download_button(
            label="Click to download",
            data=f,
            file_name=download_folder + ".zip",
            mime="application/zip",
        )
