#!usr/bin/env python
import copy

import tcod

from engine import Engine
# from entity import Entity
import entity_factory
# from map import Map
from procgen import generate_dungeon
# from input import EventHandler

def main() -> None:
    screen_width = 100
    screen_height = 80
    
    map_w = 50
    map_h = 70
    
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    
    max_monsters = 3
    
    plyr_x = int(screen_width / 2)
    plyr_y = int(screen_height / 2)
    
    tileset = tcod.tileset.load_tilesheet(
		"img/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
	)
    
    # event_handler = EventHandler()
    
    player = copy.deepcopy(entity_factory.player)
    
    engine = Engine(player=player)
    
    engine.map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_w=map_w,
        map_h=map_h,
        max_monsters=max_monsters,
        engine=engine,
    )
    
    engine.update_fov()
    # engine = Engine(event_handler=event_handler, map=map, player=player)
    
    with tcod.context.new_terminal(
		screen_width,
  		screen_height,
		tileset=tileset,
		title="Bloody Spire",
		vsync=True,
	) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            
            engine.event_handler.handle_input()
            # events = tcod.event.wait()
            
            # engine.handle_input(events)


if __name__ == "__main__":
    main()