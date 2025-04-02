
from scanner_scripts.image_segmenter.yolo_search import locate_books
from scanner_scripts.image_segmenter.gen_bounding_boxes import books_to_shelves

def item_search(data,image,type):
    # Select correct type of search function (api call & filter) 
    if type == "books":
        boxes_list = locate_books(data)
        shelves_bb = books_to_shelves(boxes_list,image) 
        
        return shelves_bb
    
    #Example for future expansion 
    elif type == "Bicycle":
        print("Not Configured")
        raise ValueError
