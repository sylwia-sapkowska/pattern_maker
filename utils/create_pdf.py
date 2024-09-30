from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Spacer
from reportlab.platypus import Image as ImagePDF
from PIL import Image, ImageDraw
import numpy as np
import os
import shutil

pixel_size = 10
minor_grid = 1
major_grid = 3

# Creates a single page of PDF chart, given cropped image and coordinates of up left pixel (stitch)
def create_page(image, upXcoord = 0, upYcoord = 0):
    height_pixels, width_pixels, _ = image.shape

    W = (width_pixels+9)//10
    H = (height_pixels+9)//10
    
    # sizes of chart on this page
    width  = (W+1) * major_grid + ((width_pixels//10) * 9 + max(0, width_pixels%10-1)) * minor_grid + width_pixels  * pixel_size
    height = (H+1) * major_grid + ((height_pixels//10) * 9 + max(0, height_pixels%10-1)) * minor_grid + height_pixels * pixel_size
    xshift = 40
    yshift = 40
    Pheight = 2 * xshift + height
    Pwidth = 2 * yshift + width

    pattern = np.zeros(shape=(Pheight, Pwidth, 3), dtype=np.uint8)

    # Added white margins to the image
    pattern[:xshift, :, :] = 255
    pattern[:, :yshift, :] = 255
    pattern[Pheight-xshift:, :, :] = 255
    pattern[:, Pwidth-yshift:, :] = 255
    
    square = major_grid + 10 * pixel_size + 9 * minor_grid
    
    # I'm drawing left and upper border of each square
    for i in range(H):
        for j in range(W):
            # Drawing 10x10 grid with coordinates (i, j)
            for k in range(i * square, min(height, (i+1)*square)):
                for l in range(j * square, min(width, (j+1)*square)):
                    dx = k - i * square
                    dy = l - j * square
                    if dx < major_grid or dy < major_grid: # major grid
                        continue
                    dx -= (major_grid - minor_grid)
                    dy -= (major_grid - minor_grid)
                    assert max(dx, dy) < 10 * (pixel_size+minor_grid)
                    if dx%(minor_grid + pixel_size) < minor_grid or dy%(minor_grid + pixel_size) < minor_grid: #minor grid
                        continue
                    # finally pixel of some color
                    dx //= (minor_grid + pixel_size)
                    dy //= (minor_grid + pixel_size)
                    if 10*i+dx < height_pixels and 10*j+dy < width_pixels:
                        pattern[xshift + k][yshift + l] = image[10*i+dx][10*j+dy]
                    
    # Drawing top and bottom lines of the whole grid
    pattern[Pheight-xshift-major_grid:Pheight-xshift, xshift:Pwidth-xshift] = 0
    pattern[yshift:Pheight-yshift, Pwidth-yshift-major_grid:Pwidth-yshift] = 0
    
    pattern = Image.fromarray(pattern)
    
    draw = ImageDraw.Draw(pattern)

    # inputting numbers on X axis
    for number_to_draw, xcoord in zip(range(10, width_pixels+1, 10), range(xshift+square, Pwidth, square)):
        draw.text((xcoord-5, yshift-15), str(upXcoord+number_to_draw), (0, 0, 0))
    if width_pixels%10:
        draw.text((Pwidth-xshift-5, yshift-15), str(width), (0, 0, 0))
        
    # similarly on Y axis
    for number_to_draw, ycoord in zip(range(0, height_pixels+1, 10), range(yshift, Pheight, square)):
        draw.text((xshift-22, ycoord-5), str(upYcoord+number_to_draw), (0, 0, 0))
    if height_pixels%10:
        draw.text((xshift-22, Pheight-yshift-5), str(height), (0, 0, 0))
    
    return pattern

# Creates pdf from the chart
def create_pdf(image, pattern, output_name="cross_stitch_pattern.pdf"):
    height, width, _ = pattern.shape

    page_width = 70 #in number of stitches
    page_height = 100 #in number of stitches

    # directory for temporary images
    if not os.path.isdir('tmp'):
        os.makedirs('tmp')

    pdf = SimpleDocTemplate(output_name, pagesize=(1000, 1370))
    story = []
    story.append(Paragraph('Cross Stitch Pattern'))

    image.save('tmp/image.jpg')
    pattern_img = Image.fromarray(pattern)
    pattern_img.save('tmp/pattern.jpg')
    
    W, H = pattern_img.size
    ratio = min(1900/W, 2700/H)/4
    story.append(ImagePDF('tmp/image.jpg', width=W*ratio, height=H*ratio))
    story.append(Spacer(width=0, height=20))
    story.append(ImagePDF('tmp/pattern.jpg', width=W*ratio, height=H*ratio))

    

    for j in range(0, height, page_height):
        for i in range(0, width, page_width):
            cropped_img = pattern[j:min(j+page_height, height), i:min(i+page_width, width)]
            pattern_page = create_page(cropped_img, i, j)
            image_path = 'tmp/tmp'+str(i)+str(j)+'.jpg'
            pattern_page.save(image_path)
            story.append(ImagePDF(image_path))
            story.append(PageBreak())

    pdf.build(story)
    shutil.rmtree('tmp')
    
    print("PDF succesfully created.")
    