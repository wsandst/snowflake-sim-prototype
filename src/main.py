import gui
from hex_grid import HexGrid

def main():
    grid = HexGrid(20, 20)

    cell = grid.get_cell(3,3)
    cell.color = (255,0,0)
    for neighbour in grid.get_neighbours(cell.q, cell.r):
        neighbour.color = (0,255,0)

    application = gui.MainApplication(grid)
    
if __name__ == "__main__":
    main()

