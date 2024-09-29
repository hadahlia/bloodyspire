from __future__ import annotations

import copy
from typing import Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from map import Map

T = TypeVar("T", bound="Entity")

class Entity:
    """
    generic entity class
    """
    def __init__(
        self, 
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
    
    def spawn(self: T, map: Map, x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        map.entities.add(clone)
        return clone
    
    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy