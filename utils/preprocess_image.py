from sklearn.cluster import KMeans
from scipy.spatial import KDTree
from PIL import Image
import numpy as np
import math

# Performs K means algorithm to reduce number of colors used, and then assignes closest DMC thread (in terms of Euclidean distance)
def perform_kmeans(image, number_of_colors, palette):
    pixels = np.float32(image.reshape(-1, 3))
    kmeans = KMeans(n_clusters=number_of_colors, random_state=0, init='k-means++').fit(pixels)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    tree = KDTree(palette)

    best_dmc_color = np.zeros((number_of_colors, 3), dtype=np.uint8)
    for i in range(number_of_colors):
        _, idx = tree.query(centers[i])
        best_dmc_color[i] = palette[idx]
        
    stitch_pattern = best_dmc_color[labels]
    stitch_pattern = stitch_pattern.reshape(image.shape).astype(np.uint8)
    return stitch_pattern

def atkinson_dither(image, palette):
    img_data = np.array(image, dtype=np.float32) 
    height, width, _ = img_data.shape
    tree = KDTree(palette)
    for y in range(height):
        for x in range(width):
            old_pixel = img_data[y, x].copy()
            
            _, idx = tree.query(old_pixel)
            new_pixel = np.array(palette[idx])
            img_data[y, x] = new_pixel

            quant_error = old_pixel - new_pixel

            if x+1 < width:
                img_data[y, x+1] += quant_error * (1/8)
            if x+2 < width:
                img_data[y, x+2] += quant_error * (1/8)
            if y+1 < height:
                if x-1 >= 0:
                    img_data[y+1, x-1] += quant_error * (1/8)
                img_data[y+1, x] += quant_error * (1/8)
                if x+1 < width:
                    img_data[y+1, x+1] += quant_error * (1/8)
            if y + 2 < height:
                img_data[y+2, x] += quant_error * (1/8)

    return np.clip(img_data, 0, 255).astype(np.uint8)

def floyd_steinberg_dither(image, palette):
    image = np.array(image, dtype=float)
    height, width, _ = image.shape

    tree = KDTree(palette)
    dmc_image = np.zeros_like(image, dtype=int)  
    
    for y in range(height):
        for x in range(width):
            old_pixel = image[y, x].copy()
            
            _, idx = tree.query(old_pixel)
            new_pixel = palette[idx]
            dmc_image[y, x] = new_pixel

            quant_error = old_pixel - new_pixel
            
            if x+1 < width:
                image[y, x+1] += quant_error * 7/16
            if x-1 >= 0 and y+1 < height:
                image[y+1, x-1] += quant_error * 3/16
            if y+1 < height:
                image[y+1, x] += quant_error * 5/16
            if x+1 < width and y+1 < height:
                image[y+1, x+1] += quant_error * 1/16
    
    return np.clip(dmc_image, 0, 255).astype(np.uint8)

# Creates kind of pixel art    
def create_pattern(image, width_stitches, number_of_colors, palette, method_of_dithering = 1):
    width, height = image.size
    height_stitches = math.ceil((height*width_stitches)/width)

    image = image.resize((width_stitches, height_stitches), Image.LANCZOS)
    img_array = np.array(image)

    if method_of_dithering == 2: # floyd-steinberg
        img_array = floyd_steinberg_dither(img_array, palette)
    if method_of_dithering == 3: # atkinson
        img_array = atkinson_dither(img_array, palette)
        
    stitch_pattern = perform_kmeans(img_array, number_of_colors, palette)
    return stitch_pattern    