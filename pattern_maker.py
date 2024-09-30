from utils.dmc import dmc_rgb_values
from utils.preprocess_image import create_pattern
from utils.create_pdf import create_pdf
import os
from PIL import Image

print("Welcome to the cross stitch pattern maker!")
print()

# file location
while True:
    image_path = input("Give a path to an image: ")
    print()

    if not os.path.isfile(image_path):
        print("Given path is incorrect! There's no such file!")
    else:
        break

image = Image.open(image_path)
width, height = image.size

# width (in the number of stitches)
while True:
    width_stitches = int(input("Input width stitches (max possible value is: " + str(width) + " stitches): "))
    print()

    if width_stitches > width:
        print("Your pattern can't be bigger than a given image!")
    else:
        break

number_of_colors = int(input("Input maximum number of colors: "))

# method of dithering
while True:
    print("What is the method of dithering of your choice?")
    print("Input:")
    print("-- 1 if none,")
    print("-- 2 if Floyd-Steinberg dither,")
    print("-- 3 if Atkinson dither.")

    method_of_dithering = int(input())
    if method_of_dithering < 1 or method_of_dithering > 3:
        print("You should pick number 1, 2, or 3.")
    else: 
        break

pattern = create_pattern(image, width_stitches, number_of_colors, dmc_rgb_values, method_of_dithering)

name_of_pdf = input("Give the name of output pdf cross stitch chart: ")

create_pdf(image, pattern, name_of_pdf)
