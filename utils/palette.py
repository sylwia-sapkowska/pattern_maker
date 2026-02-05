import pandas as pd

# Color representation
class Color:
    def __init__(self, color_id: int, name: str, rgb: tuple[int, int, int]):
        self.color_id = color_id
        self.name = name
        self.rgb = rgb

# Color palette utilities
class Palette:
    def __init__(self, palette_name: str, colors: list[Color]):
        self.palette_name = palette_name
        self.colors = colors

    def get_color_by_id(self, color_id: int) -> tuple[int, int, int] | None:
        for color in self.colors:
            if color.color_id == color_id:
                return color.rgb
        return None

    def get_color_name_by_id(self, color_id: int) -> str | None:
        for color in self.colors:
            if color.color_id == color_id:
                return color.name
        return None

    def add_color(self, color: Color) -> None:
        if all(color.color_id != existing_color.color_id for existing_color in self.colors):
            self.colors.append(color)

    def __str__(self):
        return f"Palette: {self.palette_name}, Number of colors: {len(self.colors)}"

# DMC Color Palette, loading from CSV
# CSV source: https://github.com/sharlagelfand/dmc/tree/master
class DMC(Palette):
    def __init__(self):
        dmc_df = pd.read_csv('palettes/dmc_colors.csv')
        colors_list = [
            Color(
                color_id=row['Floss#'],
                name=row['Description'],
                rgb=(row['Red'], row['Green'], row['Blue'])
            ) for _, row in dmc_df.iterrows()
        ]
        super().__init__(
            palette_name="DMC",
            colors=colors_list,
        )