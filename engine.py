from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from map import Map
from input import EventHandler

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, map: Map, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.map = map
        self.player = player
        self.update_fov()
        
    def handle_input(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            
            if action is None:
                continue
            
            action.perform(self, self.player)
            
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
        
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)
            
        context.present(console)
        
        console.clear()