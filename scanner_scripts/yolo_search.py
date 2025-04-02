import requests

headers = {"Authorization"}

API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"

def locate_books(data):
    response = requests.post(API_URL, headers=headers, data=data)
    output = response.json()
    book_boxes = [item['box'] for item in output if item['label'] == 'book']
    return book_boxes
