import time
from PIL import Image 
from scanner_scripts.image_segmenter.gen_bounding_boxes import crop_by_box
from scanner_scripts.image_segmenter.item_search import item_search

def locate_items(filename,type="books"): 
    # Locate the item in the image, with error handling

    try:
        image = Image.open(filename)
        with open(filename, "rb") as f:
            data = f.read()

        # Get list of dictionaries containing bounding box coordinates 
        locs_in_image = item_search(data,image,type)

        if len(locs_in_image) == 0:
            print(f"No {type} found in image")
            locs_in_image = None
    
    # API ERROR
    except TypeError as e: 
        print(f"Error with YOLO API - waiting then trying again. Error: {e}")
        time.sleep(1.1)
        locs_in_image = item_search(data,image,type)
        locs_in_image = None

    # OTHER ERROR 
    except Exception as e: 
        print(f"Exception in locate items: {e}")
        locs_in_image = None
        
    return image, locs_in_image 


def get_subimages(FILENAME,type):
    print("Start")

    # Get shelves bounding box, then crop into a list of images
    image, box_locs = locate_items(FILENAME)
    image_dicts = crop_by_box(image,box_locs)

    images = [x.get("image") for x in image_dicts] 
    types = [x.get("type") for x in image_dicts]

    # Format depnding on if images have been halved or not
    if types[0] == "half":
        image_lst  = [images[i:i+2] for i in range(0, len(images), 2)]
    else: 
        image_lst = images 

    if len(image_lst) > 0:
        print(f"Identified {type}")

    FILENAME =  FILENAME.split('/')[-1]
    name = FILENAME.split(".")[0]
    
    return image_lst, name