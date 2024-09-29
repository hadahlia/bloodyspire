from __future__ import annotations

import random

from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

import entity_factory
from map import Map
import tile_type

if TYPE_CHECKING:
	from entity import Entity

class RectRoom:
	def __init__(self, x: int, y: int, width: int, height: int) -> None:
		self.x1 = x
		self.y1 = y
		self.x2 = x + width
		self.y2 = y + height
	
	@property
	def center(self) -> Tuple[int, int]:
		center_x = int((self.x1 + self.x2) / 2)
		center_y = int((self.y1 + self.y2) / 2)
		
		return center_x, center_y
	
	@property
	def inner(self) -> Tuple[slice, slice]:
		"""Returns area of room as 2d array index."""
		return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

	def intersects(self, other: RectRoom) -> bool:
		return (
			self.x1 <= other.x2
			and self.x2 >= other.x1
			and self.y1 <= other.y2
			and self.y2 >= other.y1
		)

def place_entities(
	room: RectRoom, dungeon: Map, max_monsters: int,
) -> None:
    num_monsters = random.randint(0, max_monsters)
    
    for i in range(num_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)
        
        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entity_factory.shroom.spawn(dungeon, x, y) # weak enemy ! shroomy
            else:
                entity_factory.un_knight.spawn(dungeon, x, y) # strong enemy ! undead knight

def tunneler(
	start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
	"""Returns L shape between 2 points."""
	x1, y1 = start
	x2, y2 = end
	if random.random() < 0.5:
		corner_x, corner_y = x2, y1
	else:
		corner_x, corner_y = x1, y2
	
	# Generate coords
	for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
		yield x, y
	for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
		yield x, y

def generate_dungeon(
	max_rooms: int,
	room_min_size: int,
	room_max_size: int,
	map_w: int,
	map_h: int,
	max_monsters: int,
	player: Entity,
) -> Map:
    """Generates me a lil map :)"""
    dungeon = Map(map_w, map_h, entities=[player])
    rooms: List[RectRoom] = []
    for r in range(max_rooms):
        room_w = random.randint(room_min_size, room_max_size)
        room_h = random.randint(room_min_size, room_max_size)
        
        x = random.randint(0, dungeon.width - room_w - 1)
        y = random.randint(0, dungeon.height - room_h - 1)
        
        new_room = RectRoom(x, y, room_w, room_h)
         # Intersection check
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue
        
        dungeon.tiles[new_room.inner] = tile_type.floor
        
        if len(rooms) == 0:
            player.x, player.y = new_room.center
        else:
            for x, y in tunneler(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_type.floor
        
        place_entities(new_room, dungeon, max_monsters)
        
        rooms.append(new_room)
    
    return dungeon