import os
import json
from bitmap_decode import base64_2_mask

def pair_mask_2_img(annotation_path, image_path):
    mask_image_pairing = []
    annotation_list = sorted(os.listdir(annotation_path))
    image_list = sorted(os.listdir(image_path))
    
    for annotation, image in zip(annotation_list, image_list):
        bitmap = open(annotation_path + annotation)

        data = json.load(bitmap)
        objects = data["objects"]
        
        if objects:
            mask = objects[0]['bitmap']['data']
            origin = objects[0]['bitmap']['origin']
            
            mask_image_pairing.append((image_path + image, base64_2_mask(mask), origin))

        bitmap.close()
    
    return mask_image_pairing