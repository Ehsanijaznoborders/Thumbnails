import imageio
import glob
from tqdm import tqdm
from PIL import Image
import os
import logging
import logging.config

SOURCE = "/media/patient/02/VQ_GAN_Results/10_11_2021/results"
TARGET = SOURCE+"_Thumbnails"
os.makedirs(TARGET, exist_ok=True)
def crop_square(image):        
    width, height = image.size
    
    # Crop the image, centered
    new_width = min(width,height)
    new_height = new_width
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2
    return image.crop((left, top, right, bottom))
        
def scale(img, scale_width, scale_height):
    # Scale the image
    img = img.resize((
        scale_width, 
        scale_height), 
        Image.ANTIALIAS)
            
    return img

def standardize(image):
    rgbimg = Image.new("RGB", image.size)
    rgbimg.paste(image)
    return rgbimg

def fail_below(image, check_width, check_height):
    width, height = image.size
    assert width == check_width
    assert height == check_height    

files = glob.glob(os.path.join(SOURCE,"*"))

for file in tqdm(files):
   try:
     if file.endswith(('.png','.jpg','.jpeg','.JPEG','.JPG')):
        print("True")
        print('Processing : ', file)
        target = ""
        name = os.path.basename(file)
        filename, _ = os.path.splitext(name)
        img = Image.open(file)
        img = crop_square(img)
        img = scale(img, 340,340)
        # final resizing
        img = crop_square(img)
        img = scale(img, 256,256)
        file_ext = file.split('.')[1]
        
#        target = os.path.join(TARGET,"thumb_"+filename+".png")
        target = os.path.join(TARGET,filename+"."+file_ext)
        img.save(target)
   except KeyboardInterrupt:
        print("Keyboard interrupt")
        break
   except AssertionError:
        print("Assertion")
        break
   except Except as e:
        logging.warning(f"Unexpected exception while processing image source: {file}, target: {target}" , exc_info=True)
        print(e)
