
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtGui import QImage

def draw_grid(grid, size=500) -> QImage:
    """ Draw a hexagonal grid """
    image = Image.new('RGB', (size,size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    for hex in grid.all_cells:
        if hex.get_color() != (0, 0, 0):
            draw.polygon(hex.corners, hex.get_color())
        #for corner1, corner2 in zip(corners, corners[1:]):
           #draw.line((corner1[0], corner1[1], corner2[0], corner2[1]), fill=(255, 255, 255), width=3)

    return QImage(image.tobytes("raw","RGB"), image.size[0], image.size[1], QImage.Format_RGB888)