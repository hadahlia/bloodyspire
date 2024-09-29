from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from map import Map
from input import EventHandler

class Engine:
    def __init__(self, event_handler: EventHandler, map: Map, player: Entity):
        self.event_handler = event_handler
        self.map = map
        self.player = player
        self.update_fov()
    
    def handle_enemy_turn(self) -> None:
        for e in self.map.entities - {self.player}:
            print(f"The {e.name} loves you very much and dreams of a life together... ")
        
    def handle_input(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            
            if action is None:
                continue
            
            action.perform(self, self.player)
            self.handle_enemy_turn()
            self.update_fov()
    
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