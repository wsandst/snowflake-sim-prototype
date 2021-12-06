
import copy

from hex_grid import HexGrid

# No diffusion if receptive (either boundrary cell or frozen)

class SnowflakeSimulation:

    def __init__(self, grid):
        self.current_grid = grid
        self.next_grid = HexGrid(grid.width, grid.height)
        self.setup_initial_simulation()
    
    def setup_initial_simulation(self):
        self.background_vapor = 0.3
        self.vapor_addition = 0.01
        self.vapor_diffusion = 1
        for cell in self.current_grid.get_cells():
            cell.water_level = self.background_vapor
        self.current_grid.get_cell(self.current_grid.width//4, self.current_grid.height//2).water_level = 1
    
    def update(self):
        for cell, next_cell in zip(self.current_grid.get_cells(), self.next_grid.get_cells()):
            self.update_cell(cell, next_cell)
        # Set edge cells to background vapor level to introduce more vapor to the system
        for edge_cell in self.next_grid.edge_cells:
            edge_cell.water_level = self.background_vapor
        self.current_grid, self.next_grid = self.next_grid, self.current_grid

    def update_cell(self, cell, next_cell):
        if not cell.is_receptive():
            avg = 0
            for neighbour in cell.neighbours:
                if not neighbour.is_frozen():
                    avg += neighbour.water_level
            avg = avg / 6
            next_cell.water_level = cell.water_level + (self.vapor_addition/2) * (avg - cell.water_level)
        else:
            next_cell.water_level = cell.water_level + self.vapor_addition