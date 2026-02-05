from utils.palette import Color
from utils.image_processing import DEFAULT_NUM_COLORS
from typing import Any

# Class representing a single pixel in the pattern grid.
# TODO: do we need to keep its coordinates here?
class Pixel:
    def __init__(self, x: int, y: int, main_color: Color | None = None, 
                 secondary_color: Color | None = None):
        self.x = x
        self.y = y
        self.main_color = main_color
        # Optional secondary color for patterns that use blends.
        self.secondary_color = secondary_color


class ConverterConfig:
    def __init__(self, width: int, height: int | None = None, 
                 palette: Any = None, num_colors: int = DEFAULT_NUM_COLORS, 
                 function_to_process_image: Any = None):
        self.width = width
        self.height = height
        self.palette = palette
        self.num_colors = num_colors
        self.function_to_process_image = function_to_process_image

    # If height is not provided, calculate it to maintain aspect ratio.
    def _set_aspect_ratio_height(self, original_width: int, original_height: int) -> None:
        if self.height is None:
            aspect_ratio = original_height / original_width
            self.height = int(self.width * aspect_ratio)


class ImageToGridConverter:
    def __init__(self, image: Any, config: ConverterConfig = None):
        self.initial_image = image
        
        # If no config is provided, use default settings.
        if config is None:
            config = ConverterConfig(width=image.width)

        self.config = config
        self.config._set_aspect_ratio_height(image.width, image.height)

    def __call__(self) -> None:
        # Convert the image to a grid of pixels based on the configuration.
        pass