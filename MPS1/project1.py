from glob import glob

import cv2
import numpy as np

images_table = [cv2.imread(image_path) for image_path in glob("project1images/*.jpg")]
greyed_images = [cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) for image in images_table]
binarized_images = [cv2.threshold(image, 117, 255, cv2.THRESH_BINARY)[1] for image in greyed_images]
processed_images = [(np.sum(image == 255), np.sum(image == 0)) for image in binarized_images]
for index, image in enumerate(processed_images):
    print(f"Procent martenzytu dla zdjecia {index+1} to {int(100*(image[0]/(image[0]+image[1])))}")
    print(f"Natomiast procent ferrytu dla tego zdjęcia to {100-(int(100*(image[0]/(image[0]+image[1]))))} \n")
