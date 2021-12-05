
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtGui import QImage

def draw_grid(grid, size=384) -> QImage:
    """ Draw a hexagonal grid """
    image = Image.new('RGB', (size,size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    draw.rectangle((100, 100, 200, 200), fill= (0,255,255))

    return QImage(image.tobytes("raw","RGB"), image.size[0], image.size[1], QImage.Format_RGB888)