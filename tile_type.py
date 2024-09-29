from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
	[
		("ch", np.int32),
		("fg", "3B"),
		("bg", "3B"),
	]
)

tile_dt = np.dtype(
	[
		("walkok", np.bool),
		("trans", np.bool),
  		("dark", graphic_dt), # not fov
		("light", graphic_dt), # in fov
	]
)

def new_tile(
    *, 
    walkok: int,
    trans: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile type """
    return np.array((walkok, trans, dark, light), dtype=tile_dt)

# shroud is unseen tiles
SHROUD = np.array((ord(" "), (255,255,255), (0,0,0)), dtype=graphic_dt)

floor = new_tile(
	walkok=True,
 	trans=True,
  	dark=(ord(" "),(40,0,10), (0,0,0)),
	light=(ord("."),(150,0,0), (20,0,5)),
)

wall = new_tile(
	walkok=False,
 	trans=False,
  	dark=(ord(" "), (255,255,255), (45,0,10)),
	light=(ord(" "), (255,255,255), (110,0,10)),
)