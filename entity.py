from __future__ import annotations

import copy
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from map import Map

T = TypeVar("T", bound="Entity")

class Entity:
    """
    generic entity class
    """
    
    map: Map
    
    def __init__(
        self, 
        map: Optional[Map] = None,
        x: int = 0, 
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (120,120,120),
        name: str = "<Nameless>",
        collides: bool = False,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.collides = collides
        if map:
            self.map = map
            map.entities.add(self)
    
    def spawn(self: T, map: Map, x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.map = map
        map.entities.add(clone)
        return clone
    
    def place(self, x: int, y: int, map: Optional[Map] = None) -> None:
        self.x = x
        self.y = y
        if map:
            if hasattr(self, "map"):
                self.map.entities.remove(self)
            self.map = map
            map.entities.add(self)
    
    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy