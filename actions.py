from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def perform(self, engine: Engine, ent: Entity) -> None:
        raise NotImplementedError()

class EscAction(Action):
    def perform(self, engine: Engine, ent: Entity) -> None:
        raise SystemExit()

class MoveAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy
    
    def perform(self, engine: Engine, ent: Entity) -> None:
        dest_x = ent.x + self.dx
        dest_y = ent.y + self.dy
        
        if not engine.map.in_bounds(dest_x, dest_y):
            return
        if not engine.map.tiles["walkok"][dest_x, dest_y]:
            return
        
        ent.move(self.dx, self.dy)
  