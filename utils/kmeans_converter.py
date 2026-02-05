import numpy as np
from sklearn.cluster import KMeans
from utils.pattern_containers import ImageType, ConverterConfig, Grid
from utils.color_utils import map_colors_to_palette, convert_rgb_to_cielab

def KMeansColorQuantization(image: ImageType, config: ConverterConfig) -> Grid:
    # Resize the image to the target dimensions specified in the config.
    image = image.resize((config.width, config.height))

    # Convert the image to a numpy array and reshape it for KMeans.
    pixels = list(map(convert_rgb_to_cielab, np.float32(image.reshape(-1, 3))))
    kmeans = KMeans(n_clusters=config.number_of_colors, random_state=0, init='k-means++').fit(pixels)
    
    # Map the cluster centers to the closest colors in the palette.
    palette_colors = map_colors_to_palette(kmeans.cluster_centers_, config.palette, config.include_blends)

    # Create a grid and fill it with the corresponding colors from the palette.
    grid = Grid(config.width, config.height)
    for i, label in enumerate(kmeans.labels_):
        x = i % config.width
        y = i // config.width
        grid.pixels[y][x] = palette_colors[label]

    return grid