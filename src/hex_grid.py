import math

HEX_SIZE = 5
HEX_OFFSET = 50
AA_LEVEL = 2

class Cell:
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.neighbours = []

        self.water_level = 0
        self.diffusion_content = 0

    def get_pixel_coord(self):
        x = HEX_SIZE * (math.sqrt(3) * self.q  +  math.sqrt(3)/2 * self.r)
        y = HEX_SIZE * (3./2 * self.r)
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

    def get_color(self):
        if self.water_level >= 0.6:
            return ((int)(127*self.water_level), (int)(210*self.water_level), (int)(245*self.water_level))
        else:
            return (0, 0, 0)


class HexGrid:
    """ Hexagonal grid, represented using Axial coordinates. """
    def __init__(self, width, height):
        self.cells = [None for _ in range((width+width//2)*height)]
        self.width = width
        self.height = height
        for r in range(self.height):
            r_offset = math.floor(r/2.0)
            for q in range(0-r_offset, self.width-r_offset):
                self.set_cell(q, r, Cell(q, r))
        for cell in self.get_cells():
            cell.neighbours = self.get_neighbours(cell.q, cell.r)
        self.edge_cells = self.get_edge_cells()

    def get_cell(self, q, r):
        return self.cells[q*self.height + r]

    def set_cell(self, q, r, cell):
        self.cells[q*self.height + r] = cell

    def get_cells(self):
        for r in range(self.height):
            r_offset = math.floor(r/2.0)
            for q in range(0-r_offset, self.width-r_offset):
                yield self.get_cell(q, r)

    def inside_bounds(self, q, r):
        return (q < self.width and r < self.height and self.get_cell(q,r) != None)

    def get_neighbours(self, q, r):
        neighbours = []
        neighbour_coords = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        for coord in neighbour_coords:
            nq = q + coord[0]
            nr = r + coord[1]
            if self.inside_bounds(nq, nr):
                neighbours.append(self.get_cell(nq, nr))
        return neighbours

    def get_edge_cells(self):
        edge_cells = []
        for cell in self.get_cells():
            if len(self.get_neighbours(cell.q, cell.r)) < 6:
                edge_cells.append(cell)
        return edge_cells



def hex_corner(center, size, i):
    angle_deg = 60 * i - 30
    angle_rad = math.pi / 180 * angle_deg
    return (center[0] + size * math.cos(angle_rad) + HEX_OFFSET, 
            center[1] + size * math.sin(angle_rad) + HEX_OFFSET)