from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from entity import Entity
from map import Map
from input import EventHandler

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, map: Map, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.map = map
        self.player = player
        
    def handle_input(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            
            if action is None:
                continue
            
            action.perform(self, self.player)
    
    def render(self, console: Console, context: Context) -> None:
        self.map.render(console)
        
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)
            
        context.present(console)
        
        console.clear()