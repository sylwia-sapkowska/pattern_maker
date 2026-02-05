from utils.palette import Palette, Color, DMC
from utils.image_processing import DEFAULT_NUM_COLORS, KMeansColorQuantization
from typing import Any, TypeAlias, Callable, Self

# Class representing a single pixel in the pattern grid.
# TODO: do we need to keep its coordinates here?
class Pixel:
    def __init__(self, int, main_color: Color | None = None, 
                 secondary_color: Color | None = None):
        if not self.check_colors(main_color, secondary_color):
            raise ValueError("Main and secondary colors must be different or secondary color must be None.")
        self.main_color = main_color
        # Optional secondary color for patterns that use blends.
        self.secondary_color = secondary_color

    @staticmethod
    def check_colors(main, secondary) -> bool:
        return secondary is None or (main is not None and main != secondary)

Coordinate: TypeAlias = tuple[int, int]
Image: TypeAlias = Any # TODO: Replace with actual image type.
class BackStitch:
    def __init__(self, color: Color, start: Coordinate, end: Coordinate):
        if start == end:
            raise ValueError("Start and end coordinates for backstitch cannot be the same.")
        self.color = color
        self.start = start
        self.end = end

class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.colors_list: list[Color] = []
        self.pixels = [[Pixel(int) for _ in range(width)] for _ in range(height)]
        self.backstitches: list[BackStitch] = []

    def get(self, x: int, y: int) -> Pixel:
        try:
            return self.pixels[y][x]
        except IndexError:
            raise IndexError("Pixel coordinates out of bounds.")

class ConverterConfig:
    def __init__(self, width: int, height: int | None = None, 
                 palette: Palette = DMC, num_colors: int = DEFAULT_NUM_COLORS, 
                 function_to_process_image: Callable[[Image, Self], Grid] = KMeansColorQuantization,
                 include_blends: bool = False,
                 function_to_add_backstitch: Callable[[Image, Grid], None] | None = None):
        self.width = width
        self.height = height
        self.palette : Palette = palette
        self.num_colors = num_colors
        self.function_to_process_image = function_to_process_image
        self.include_blends = include_blends
        self.backstitch_function = function_to_add_backstitch

    # If height is not provided, calculate it to maintain aspect ratio.
    def _set_aspect_ratio_height(self, original_width: int, original_height: int) -> None:
        if self.height is None:
            aspect_ratio = original_height / original_width
            self.height = int(self.width * aspect_ratio)

class ImageToGridConverter:
    def __init__(self, image: Image, config: ConverterConfig = None):
        self.initial_image = image
        
        # If no config is provided, use default settings.
        if config is None:
            config = ConverterConfig(width=image.width)

        self.config = config
        self.config._set_aspect_ratio_height(image.width, image.height)

        self.grid = None

    def __call__(self) -> Grid:
        # If the grid has already been computed, return it.
        if self.grid is not None:
            return self.grid

        # Convert the image to a grid of pixels based on the configuration.
        try:
            self.grid = self.config.function_to_process_image(
                self.initial_image, 
                self.config
            )
            # Generate backstitching if applies.
            if self.config.backstitch_function is not None:
                self.config.backstitch_function(self.initial_image, self.grid)
            return self.grid
        except Exception as e:
            raise RuntimeError("Error processing image with the provided function.") from e

    def generate_pdf(self):
        pass