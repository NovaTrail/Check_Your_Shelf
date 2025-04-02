import os 
import concurrent.futures
import pandas as pd 

def temp_save_image(image):
    # Define a local directory to save the uploaded image
    save_directory = "store"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    # Save the image locally
    
    temp_name = "bookshelf_temp.jpg" 
    image.save(f"{save_directory}/{temp_name}")


def get_dual_image_results(_image,name):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(_image, _image[0], name, 'left')
        future2 = executor.submit(_image, _image[1], name, 'right')
    
    resale1, all_df1 = future1.result()
    resale2, all_df2 = future2.result()

    try:
        all_df = pd.concat([all_df1,all_df2], ignore_index=True)
        resale = pd.concat([resale1,resale2], ignore_index=True)  
    except ValueError as ve:
        print(ve)
        all_df = None
        resale = None
    
    return resale, all_df