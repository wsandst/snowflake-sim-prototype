import gui
from hex_grid import HexGrid

import queue

from sim import SnowflakeSimulation

# Color cells based on breadth first search
def visit_cells(grid, start_cell):
    cell_queue = queue.Queue()
    cell_queue.put(start_cell)
    while(not cell_queue.empty()):
        cell = cell_queue.get()
        cell.color = (0, cell.depth*3, 0)
        for neighbour in grid.get_neighbours(cell.q, cell.r):
            if not neighbour.visited:
                neighbour.visited = True
                neighbour.depth = cell.depth + 1
                cell_queue.put(neighbour)

    

def main():
    sim = SnowflakeSimulation(HexGrid(50, 50))
        
    application = gui.MainApplication(sim)
    
if __name__ == "__main__":
    main()

