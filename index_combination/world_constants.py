import pandas as pd
import numpy as np
import itertools
import yaml

SOFTWARE_CAPTION = "SYL Index combination visualizer"
LOGO_PATH = "input_folder/logo2.png"

def get_indices(index_set):
	"""
	index set: nextera, neb
	"""
	main_dict = yaml.load(open("input_folder/index_list.yaml"),
							Loader = yaml.FullLoader)

	i7_list = main_dict["index"][index_set]["i7"]
	i5_list = main_dict["index"][index_set]["i5"]

	return i7_list, i5_list

I7_LIST, I5_LIST = get_indices("nextera")
NROWS, NCOLS = len(I7_LIST), len(I5_LIST)

BLACK = (0, 0, 0)
LINECOLOR = (255,111,105)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BEIGE = (255,238,173)
BEIGE2 = (255,247,128)

# This sets the WIDTH and HEIGHT of each grid location
GRID_WIDTH = 20
GRID_HEIGHT = 20

# This sets the margin between each cell
MARGIN_THICKNESS = 1

WINDOW_HEIGHT = int(((MARGIN_THICKNESS + GRID_HEIGHT) * NROWS )*1.1)
WINDOW_WIDTH = int(((MARGIN_THICKNESS + GRID_WIDTH) * NCOLS )*1.3)
WINDOW_SIZE = [WINDOW_HEIGHT, WINDOW_WIDTH]

FEATURE_MAPVALUE = {
	"ALREADY CHOSEN": 100,
	"WE ARE CHOOSING THIS": 10
}

COLOR_MAP = {
	0: BEIGE, # empty
	1: BEIGE2, # empty
	10: GREEN, # WE ARE CHOOSING THIS
	100: RED   # ALREADY CHOSEN
}

CLICK_BUTTON = {
	"LEFT": 1,
	"MIDDLE": 2
}



