from PIL import Image, ImageDraw
from typing import Tuple
import numpy as np

# Define dimensions
ROWS = 100 #7
COLUMNS = 100 #52
DIM = 50
WIDTH = COLUMNS * DIM
HEIGHT = ROWS * DIM
grey = (200, 200, 200)  # Gray color (RGB values)
light_green =  (154, 237, 175)
medium_green = (102, 204, 136)
dark_green = (51, 153, 102)
color_map = {0:grey, 1:light_green, 2:medium_green, 3:dark_green}

def generate_matrix(rows: int=ROWS, columns: int=COLUMNS) -> list[list[int]]:
    # Load the image
    image_path = 'j.png'
    img = Image.open(image_path)
    # Convert the image to grayscale
    img_gray = img.convert('L')
    img_gray_inverted = Image.eval(img_gray, lambda x: 255 - x)
    img_resized = img_gray_inverted.resize((columns, rows), Image.ANTIALIAS)

    # Convert the resized image to a matrix
    matrix = np.array(img_resized)
    # Define thresholds for bucketing
    low_threshold = 64  # Adjust as needed
    mid_threshold = 128  # Adjust as needed
    high_threshold = 192  # Adjust as needed
    # Bucket the values in the matrix into 4 different values (0, 1, 2, 3)
    matrix[matrix < low_threshold] = 0
    matrix[(matrix >= low_threshold) & (matrix < mid_threshold)] = 1
    matrix[(matrix >= mid_threshold) & (matrix < high_threshold)] = 2
    matrix[matrix >= high_threshold] = 3
    return matrix.tolist()  # Convert to nested list for easy handling

def add_squares(img: Image.Image, matrix: list[list[int]]):
    draw = ImageDraw.Draw(img)
    for y in range(ROWS):
        for x in range(COLUMNS):
            value = matrix[y][x]
            square_color=color_map[value]
            square_coords = (x *DIM, y * DIM, (x + 1) * DIM, (y + 1) * DIM)
            draw.rectangle(square_coords, fill=square_color, outline='white', width=2)
    return draw

def main():
    img = Image.new('RGB', (WIDTH, HEIGHT), color='white')
    matrix = generate_matrix()
    draw = add_squares(img, matrix)
    # Save the image as PNG
    img.save('pix_j.png')

if __name__ == "__main__":
    main()
