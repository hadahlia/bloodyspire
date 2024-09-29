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

class ActionWithDir(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()
        
        self.dx = dx
        self.dy = dy
    
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()

class SwordAction(ActionWithDir):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.map.get_colliding_entity(dest_x, dest_y)
        if not target:
            return # no attack
        
        print(f"You attack {target.name}!")

class MoveAction(ActionWithDir):
    
    def perform(self, engine: Engine, ent: Entity) -> None:
        dest_x = ent.x + self.dx
        dest_y = ent.y + self.dy
        
        if not engine.map.in_bounds(dest_x, dest_y):
            return # out of bounds
        if not engine.map.tiles["walkok"][dest_x, dest_y]:
            return # blcked by tile
        if engine.map.get_colliding_entity(dest_x, dest_y):
            return # blocked by entity
        
        ent.move(self.dx, self.dy)

class BumpAction(ActionWithDir):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        
        if engine.map.get_colliding_entity(dest_x, dest_y):
            return SwordAction(self.dx, self.dy).perform(engine, entity)
        
        else:
            return MoveAction(self.dx, self.dy).perform(engine, entity)
  