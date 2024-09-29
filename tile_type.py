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
		("dark", graphic_dt),
	]
)

def new_tile(
    *, 
    walkok: int,
    trans: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile type """
    return np.array((walkok, trans, dark), dtype=tile_dt)


floor = new_tile(
	walkok=True, trans=True, dark=(ord("."), (150,0,0), (0,0,0)),
)

wall = new_tile(
	walkok=False, trans=False, dark=(ord(" "), (255,255,255), (100,0,10)),
)