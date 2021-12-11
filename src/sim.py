
import copy
import time

from hex_grid import Cell, HexGrid


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

        for cell in self.current_grid.all_cells:
            cell.water_level = self.background_vapor

        start_cell = self.current_grid.get_cell(self.current_grid.width//4, self.current_grid.height//2)
        next_start_cell = self.next_grid.get_cell(self.current_grid.width//4, self.current_grid.height//2)
        next_start_cell.receptive = True
        start_cell.water_level = 1
        start_cell.receptive = True
        self._update_receptive_due_to_frozen(start_cell)
        self._update_receptive_due_to_frozen(next_start_cell)
        #self.current_grid.get_cell(self.current_grid.width//4, self.current_grid.height//2).water_level = 1

    

        self.iteration_count = 0
    

    def _update_receptive_due_to_frozen(self, cell: Cell):
        for neigh in cell.neighbours:
            neigh.receptive = True


    def update(self):
        start = time.time()
        #for cell, next_cell in zip(self.current_grid.all_cells, self.next_grid.all_cells):
        #    cell.mark_if_receptive()
        for cell, next_cell in zip(self.current_grid.all_cells, self.next_grid.all_cells):
            self.update_cell(cell, next_cell)
        # Set edge cells to background vapor level to introduce more vapor to the system
        for edge_cell in self.next_grid.edge_cells:
            edge_cell.water_level = self.background_vapor
        self.current_grid, self.next_grid = self.next_grid, self.current_grid
        self.iteration_count += 1
        end = time.time()
        #print("Update took: ", end - start)

    def update_cell(self, cell, next_cell):
        if cell.receptive:
            diffusion_particip = 0
            diffusion_nonparticip = cell.water_level + self.vapor_addition
        else:
            diffusion_particip = cell.water_level
            diffusion_nonparticip = 0

        avg = 0
        for neighbour in cell.neighbours:
            if not neighbour.receptive:
                avg += neighbour.water_level

        avg = avg / 6
        diffusion_particip = diffusion_particip + (self.vapor_diffusion/2) * (avg - diffusion_particip)

        started_frozen = next_cell.is_frozen()
        next_cell.water_level = diffusion_nonparticip + diffusion_particip
        ended_frozen = next_cell.is_frozen()
        if started_frozen != ended_frozen:
            self._update_receptive_due_to_frozen(next_cell)
