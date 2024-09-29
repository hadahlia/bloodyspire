import numpy as np #type: ignore
from tcod.console import Console

import tile_type

class Map:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_type.wall, order="F")
        
        # self.tiles[30:33, 22] = tile_type.wall
    
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def render(self, console: Console) -> None:
        console.rgb[0: self.width, 0: self.height] = self.tiles["dark"]