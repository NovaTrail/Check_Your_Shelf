def split_box_in_half(image_width,current_group):
    half_width = image_width / 2
    current_group1 = current_group.copy()
    current_group2 = current_group.copy()

    current_group1['xmin'] = 0
    current_group1['xmax'] = int(half_width*1.03)
    current_group1['type'] = 'half'

    current_group2['xmin'] = int(half_width*0.97)
    current_group2['xmax'] = image_width
    current_group2['type'] = 'half'
    return current_group1 , current_group2

def books_to_shelves(boxes,image):
    """
    Groups overlapping boxes based on their height.
    """
    image_width, image_height = image.size
    half_images_flag =  len(boxes) > 18
    boxes = sorted(boxes, key=lambda b: b['ymin'])  # Sort by ymin
    grouped_boxes = []

    current_group = boxes[0]

    for box in boxes[1:]:
        current_group['xmin'] = 0
        current_group['xmax'] = image_width
        current_group['type'] = "full"
        # Check for overlap in height
        if box['ymin'] <= current_group['ymax']*0.9:
            # Merge boxes by extending the current group's ymin and ymax
            current_group['ymin'] = min(current_group['ymin'], box['ymin'])
            current_group['ymax'] = max(current_group['ymax'], box['ymax'])

        else:
            # No longer overlap, save current group and start a new one
            if half_images_flag:
                cg1, cg2 = split_box_in_half(image_width,current_group)
                grouped_boxes.extend([cg1,cg2])
            else: 
                grouped_boxes.append(current_group)

            current_group = box
            
    # Add the last group    
    if half_images_flag:
        cg1, cg2 = split_box_in_half(image_width,current_group)
        grouped_boxes.extend([cg1,cg2])
    else: 
        grouped_boxes.append(current_group)
    return grouped_boxes

def crop_by_box(image, boxes):
    """
    Crops the image to the size of each bounding box
    """
    image_width, image_height = image.size
    cropped_images = []

    for bb in boxes:
        ymax = bb['ymin'] - (image_height * 0.03)
        if ymax < 0 :
            ymax = 0
        ymin = bb['ymax']

        cropped = image.crop((bb['xmin'], ymax, bb['xmax'], ymin))
        cropped_images.append({"image":cropped,"type":bb['type']})

    return cropped_images