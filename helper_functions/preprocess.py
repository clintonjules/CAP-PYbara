import os
import numpy as np
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
            image_pixels = image_file_2_pixels(image_path + image)
            normalized_image = normalize_image(image_pixels)
            
            # Include image_shape in the tuple
            image_shape = normalized_image.shape
                     
            mask_image_pairing.append((normalized_image, base64_2_mask(mask), origin, image_shape))

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

def align_mask(mask, origin, image_shape):
    aligned_mask = np.zeros(image_shape[:2], dtype=np.float32)  # Create a blank mask with the same size as the image
    x_start, y_start = origin

    # Ensure the mask does not exceed the image boundaries
    y_end = min(y_start + mask.shape[0], image_shape[0])
    x_end = min(x_start + mask.shape[1], image_shape[1])

    # Adjust mask dimensions if it extends beyond the image
    mask = mask[:y_end - y_start, :x_end - x_start]

    aligned_mask[y_start:y_end, x_start:x_end] = mask  # Place the mask on the blank canvas
    return aligned_mask
