import math
HEX_SIZE = 4
HEX_OFFSET = 50
AA_LEVEL = 2

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []
        self.receptive = False
        self.water_level = 0
        self.diffusion_content = 0
        self.corners = self.get_corners()
        self.corners.append(self.corners[0])

    def get_pixel_coord(self):
        x = HEX_SIZE * math.sqrt(3) * (self.x + 0.5 * (self.y % 2 == 1))
        y = HEX_SIZE * 3/2 * self.y
        return (x, y)

    def get_corners(self):
        center = self.get_pixel_coord()
        return [hex_corner(center, HEX_SIZE, i) for i in range(6)]

    def is_frozen(self):
        return self.water_level >= 1

    def is_receptive(self):
        """ Is the cell receptive, ie frozen or next to a frozen cell"""
        if self.is_frozen():
            return True
        else:
            for neighbour in self.neighbours:
                if neighbour.is_frozen():
                    return True
        return False

    def mark_if_receptive(self):
        self.receptive = self.is_receptive()

    def get_color(self):
        if self.water_level >= 0.6:
            return ((int)(127*self.water_level), (int)(210*self.water_level), (int)(245*self.water_level))
        else:
            return (0, 0, 0)


class HexGrid:
    """ Hexagonal grid, represented using Axial coordinates. """
    def __init__(self, width, height):
        self.cells = [None for _ in range(width*height)]
        self.width = width
        self.height = height

        for y in range(self.height):
            for x in range(self.height):
                self.set_cell(x, y, Cell(x, y))
        for cell in self.get_all_cells():
            cell.neighbours = self.get_neighbours(cell.x, cell.y)
        self.edge_cells = self.get_edge_cells()
        self.all_cells = self.get_all_cells()

    def get_cell(self, x, y):
        return self.cells[y*self.height + x]

    def set_cell(self, x, y, cell):
        self.cells[y*self.height + x] = cell

    def get_all_cells(self):
        all_cells = list()
        for y in range(self.height):
            for x in range(self.width):
                all_cells.append(self.get_cell(x, y))
        return all_cells

    def inside_bounds(self, x, y):
        return (x < self.width and y < self.height and self.get_cell(x,y) != None)

    def get_neighbours(self, x, y):
        neighbours = []
        if (y % 2 == 0): # Even
            neigh_coords = [(+1,  0), (0, -1), (-1, -1), (-1,  0), (-1, +1), ( 0, +1)]
        else: # Odd
            neigh_coords = [(+1,  0), (+1, -1), (0, -1), (-1,  0), (0, +1), (+1, +1)]
        for coord in neigh_coords:
            if self.inside_bounds(x + coord[0], y + coord[1]):
                neighbours.append(self.get_cell(x + coord[0], y + coord[1]))
        return neighbours

    def get_edge_cells(self):
        edge_cells = []
        for cell in self.get_all_cells():
            if len(self.get_neighbours(cell.x, cell.y)) < 6:
                edge_cells.append(cell)
        return edge_cells

def hex_corner(center, size, i):
    angle_deg = 60 * i - 30
    angle_rad = math.pi / 180 * angle_deg
    return (center[0] + size * math.cos(angle_rad) + HEX_OFFSET, 
            center[1] + size * math.sin(angle_rad) + HEX_OFFSET)