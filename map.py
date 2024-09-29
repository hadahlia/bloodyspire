from __future__ import annotations

from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np #type: ignore
from tcod.console import Console

import tile_type

if TYPE_CHECKING:
    from entity import Entity

class Map:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_type.wall, order="F")
        
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.seen = np.full((width, height), fill_value=False, order="F")
        # self.tiles[30:33, 22] = tile_type.wall
    
    def get_colliding_entity(self, lx: int, ly: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.collides and entity.x == lx and entity.y == ly:
                return entity
        
        return None
    
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def render(self, console: Console) -> None:
        console.rgb[0: self.width, 0: self.height] = self.tiles["dark"]
        """
        Renders the map. if tile is visible, draw it light
        if not visible, but explored, be dark colors
        default is SHROUD.
        """
        
        console.rgb[0: self.width, 0:self.height] = np.select(
			condlist=[self.visible, self.seen],
   			choicelist=[self.tiles["light"], self.tiles["dark"]],
			default=tile_type.SHROUD
		)
        
        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)
        