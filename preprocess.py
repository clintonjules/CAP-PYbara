import os
import cv2
import json
from bitmap_decode import base64_2_mask, overlay_mask


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
            
            # mask_image_pairing.append((image_path + image, base64_2_mask(mask), origin))
            image = image_file_2_pixels(image_path + image)
                     
            mask_image_pairing.append((normalize_image(image), base64_2_mask(mask), origin))

        bitmap.close()
    
    return mask_image_pairing

def image_file_2_pixels(image):
    return cv2.imread(image)

def normalize_image(image):
    return image.astype('float32') / 255.0

def annotate_images(mask_image_pairs_list):
    annotated_images = []
    
    for pair in mask_image_pairs_list:
        # Load your image
        img, mask, start = pair
        original_image = cv2.imread(img)

        # Overlay the mask on the image
        result_image = overlay_mask(original_image, mask, start)

        annotated_images.append(result_image)
        
    return annotated_images
