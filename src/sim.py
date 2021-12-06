
import copy

from hex_grid import HexGrid

# No diffusion if receptive (either boundrary cell or frozen)

class SnowflakeSimulation:

    def __init__(self, grid, alpha, beta, gamma):
        self.current_grid = grid
        self.next_grid = HexGrid(grid.width, grid.height)
        self.setup_initial_simulation(alpha, beta, gamma)
    
    def setup_initial_simulation(self, alpha, beta, gamma):
        #self.background_vapor = 0.3 # Beta
        #self.vapor_addition = 0.001 # Gamma
        #self.vapor_diffusion = 1 # Alpha
        self.background_vapor = beta # Beta
        self.vapor_addition = gamma # Gamma
        self.vapor_diffusion = alpha # Alpha
        for cell in self.current_grid.get_cells():
            cell.water_level = self.background_vapor
        self.current_grid.get_cell(self.current_grid.width//4, self.current_grid.height//2).water_level = 1
        self.iteration_count = 0
    
    def update(self):
        for cell, next_cell in zip(self.current_grid.get_cells(), self.next_grid.get_cells()):
            self.update_cell(cell, next_cell)
        # Set edge cells to background vapor level to introduce more vapor to the system
        for edge_cell in self.next_grid.edge_cells:
            edge_cell.water_level = self.background_vapor
        self.current_grid, self.next_grid = self.next_grid, self.current_grid
        self.iteration_count += 1

    def update_cell(self, cell, next_cell):
        if cell.is_receptive():
            diffusion_particip = 0
            diffusion_nonparticip = cell.water_level + self.vapor_addition
        else:
            diffusion_particip = cell.water_level
            diffusion_nonparticip = 0

        avg = 0
        for neighbour in cell.neighbours:
            if not neighbour.is_receptive():
                avg += neighbour.water_level

        avg = avg / 6
        diffusion_particip = diffusion_particip + (self.vapor_diffusion/2) * (avg - diffusion_particip)

        next_cell.water_level = diffusion_nonparticip + diffusion_particip