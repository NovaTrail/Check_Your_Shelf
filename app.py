#streamlit run app.py
import streamlit as st
import pandas as pd
from PIL import Image

from main_proc import analyse_image, clear_temp_files 
from scanner_scripts.image_segmenter import extract_items
from support_functions import temp_save_image, get_dual_image_results

st.set_page_config(page_title="Book Scanner", page_icon="📖")

# Title of the app
st.title("Check YoShelf 📖")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)


clear_button = st.button("Clear all")  

if clear_button:
    st.rerun() 

go_button = st.button("Scan Image")

if go_button and uploaded_file is not None: 
    st.image(image, caption="Uploaded Image", use_container_width=True)
    temp_save_image()
    image_lst, name = extract_items.get_subimages("store/bookshelf_temp.jpg","books")

    search_dfs = {}  
    shelf_count = 0 
    results = []
    
    for _image in image_lst:
        shelf_count += 1 

        if isinstance(_image, list): 
            columns = st.columns(2)
            resale, all_df = get_dual_image_results(_image, name)
            resale["Shelf"] = shelf_count
            results.append(resale)
            with columns[0]:
                st.image(_image[0], caption=f"Shelf {shelf_count} Left", use_container_width=True)
            with columns[1]: 
                st.image(_image[1], caption=f"Shelf {shelf_count} Right", use_container_width=True)
            
            with st.expander(f"Shelf {shelf_count}:"):
                st.write(all_df)

        else:
            st.image(_image, caption=f"Shelf {shelf_count}", use_container_width=True)
            resale, all_df = analyse_image(_image,name)
            #search_dfs[f"s{idx + 1}"] = out
            resale['shelf'] = shelf_count
            results.append(resale)

            with st.expander(f"Shelf {shelf_count}:"):
                st.write(all_df)
    
    clear_temp_files()
    if len(results) > 0:
        resale_df = pd.concat(results, ignore_index=True)  
    else: 
        resale_df = None

    st.subheader("Potential for Resale 💎")
    st.write(resale_df)
