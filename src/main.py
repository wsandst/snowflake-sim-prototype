import gui
from hex_grid import HexGrid

import queue

from sim import SnowflakeSimulation

def main():
    sim = SnowflakeSimulation(HexGrid(150, 150), 1, 0.4, 0.0001)
        
    application = gui.MainApplication(sim)
    
if __name__ == "__main__":
    main()

