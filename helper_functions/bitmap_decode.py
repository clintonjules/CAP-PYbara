import numpy as np
import cv2, zlib, base64, io
from PIL import Image


def base64_2_mask(s: str) -> np.ndarray:
    '''
    Converts base64 string to a mask array
    
    Input:
        s - base64 string
        
    Return:
        mask - NumPy N-dimensional array of boolean values
    '''

    z = zlib.decompress(base64.b64decode(s))
    n = np.fromstring(z, np.uint8)
    mask = cv2.imdecode(n, cv2.IMREAD_UNCHANGED)[:, :, 3].astype(bool)
    return mask

def mask_2_base64(mask: np.ndarray) -> str:
    '''
    Converts mask array to base64 string
    
    Input:
        mask - NumPy N-dimensional array of boolean values
        
    Return:
        s - base64 string
    '''
    img_pil = Image.fromarray(np.array(mask, dtype=np.uint8))
    img_pil.putpalette([0,0,0,255,255,255])
    bytes_io = io.BytesIO()
    img_pil.save(bytes_io, format='PNG', transparency=0, optimize=0)
    bytes = bytes_io.getvalue()
    
    return base64.b64encode(zlib.compress(bytes)).decode('utf-8')

def overlay_mask(image: np.ndarray, mask: np.ndarray, origin: tuple[int]) -> np.ndarray:
    '''
    Create an image with the specified mask
    
    Input:
        image - NumPy N-dimensional array of the image data
        mask - NumPy N-dimensional array of boolean values
        origin - Tuple of the origin of the bitmap mask
        
    Return:
        masked image - NumPy N-dimensional array of the masked image data
    '''
    
    # Ensure the mask is the same size as the image
    full_size_mask = np.zeros(image.shape[:2], dtype=bool)
    
    # Set the mask at the correct position
    full_size_mask[origin[1]:origin[1]+mask.shape[0], origin[0]:origin[0]+mask.shape[1]] = mask
    
    # Overlay the mask
    masked_image = image.copy()
    masked_image[full_size_mask] = (0, 255, 0)  # overlay in green

    return masked_image
