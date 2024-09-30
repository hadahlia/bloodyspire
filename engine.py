from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    from map import Map

class Engine:
    map: Map
    
    def __init__(self, player: Entity):
        self.event_handler: EventHandler = EventHandler(self)
        # self.map = map
        self.player = player
        # self.update_fov()
    
    def handle_enemy_turn(self) -> None:
        for e in self.map.entities - {self.player}:
            print(f"The {e.name} loves you very much and dreams of a life together... ")
    
    def update_fov(self) -> None:
        self.map.visible[:] = compute_fov(
			self.map.tiles["trans"],
			(self.player.x, self.player.y),
			radius=8,
		)
        self.map.seen |= self.map.visible
    
    def render(self, console: Console, context: Context) -> None:
        self.map.render(console)
        
        context.present(console)
        
        console.clear()