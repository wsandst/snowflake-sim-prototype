import gui
from hex_grid import HexGrid

import queue

from sim import SnowflakeSimulation

def main():
    sim = SnowflakeSimulation(HexGrid(150, 150), alpha=1, beta=0.4, gamma=0.0001)
        
    application = gui.MainApplication(sim)
    
if __name__ == "__main__":
    main()

