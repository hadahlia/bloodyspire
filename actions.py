from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity
    
    @property
    def engine(self) -> Engine:
        """return the engine an action belongs to"""
        return self.entity.map.engine
    
    def perform(self) -> None:
        """
        Perform this action with the objects it needs
        self.engine is the scope of the action
        
        self.entity is the object performing the action?
        """
        raise NotImplementedError()

class EscAction(Action):
    def perform(self) -> None:
        raise SystemExit()

class ActionWithDir(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)
        
        self.dx = dx
        self.dy = dy
    
    @property
    def d_coord(self) -> Tuple[int, int]:
        """x and y destinations"""
        return self.entity.x + self.dx, self.entity.y + self.dy
    
    @property
    def colliding_ent(self) -> Optional[Entity]:
        return self.engine.map.get_colliding_entity(*self.d_coord)
    
    def perform(self) -> None:
        raise NotImplementedError()

class SwordAction(ActionWithDir):
    def perform(self) -> None:
        target = self.colliding_ent
        # dest_x = entity.x + self.dx
        # dest_y = entity.y + self.dy
        # target = engine.map.get_colliding_entity(dest_x, dest_y)
        if not target:
            return # no attack
        
        print(f"You attack {target.name}!")

class MoveAction(ActionWithDir):
    
    def perform(self) -> None:
        dest_x, dest_y = self.d_coord
        
        if not self.engine.map.in_bounds(dest_x, dest_y):
            return # out of bounds
        if not self.engine.map.tiles["walkok"][dest_x, dest_y]:
            return # blcked by tile
        if self.engine.map.get_colliding_entity(dest_x, dest_y):
            return # blocked by entity
        
        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDir):
    def perform(self) -> None:
        if self.colliding_ent:
            return SwordAction(self.entity, self.dx, self.dy).perform()
        # dest_x = entity.x + self.dx
        # dest_y = entity.y + self.dy
        
        # if engine.map.get_colliding_entity(dest_x, dest_y):
        #     return SwordAction(self.dx, self.dy).perform(engine, entity)
        
        else:
            return MoveAction(self.entity, self.dx, self.dy).perform()
  