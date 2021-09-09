from world_constants import *
import pandas as pd
import numpy as np
import pygame
import subprocess
from tkinter import filedialog, Tk

def initiate_grid():
	_grid = np.zeros((NROWS, NCOLS))
	return _grid

def draw_grid(surface, grid):
	for row in range(NROWS):
		for column in range(NCOLS):
			COLOR_KEY = grid[row][column]
			color = COLOR_MAP[COLOR_KEY]
			pygame.draw.rect(surface,
							 color,
							 [(MARGIN_THICKNESS + GRID_WIDTH) * column + MARGIN_THICKNESS,
							  (MARGIN_THICKNESS + GRID_HEIGHT) * row + MARGIN_THICKNESS,
							  GRID_WIDTH,
							  GRID_HEIGHT])

def draw_lines(surface):
	for col in range(0, NCOLS, 8):

		x_pos = (MARGIN_THICKNESS + GRID_WIDTH) * col
		pygame.draw.line(surface, LINECOLOR, (x_pos, 0), (x_pos, WINDOW_HEIGHT))

	for row in range(0, NROWS, 8):
		y_pos = (GRID_HEIGHT + MARGIN_THICKNESS) * row
		pygame.draw.line(surface, LINECOLOR, (0, y_pos), (WINDOW_WIDTH, y_pos))

def find_column_header_linenumber(sample_sheet_path):
	bashCommand = "cat " + sample_sheet_path + " | nl | grep -B 1  Sample_ID | head -1 | cut -f1"
	pipe = subprocess.Popen(bashCommand, shell = True, stdout=subprocess.PIPE)
	linenumber = int(pipe.communicate()[0].decode("utf-8"))
	return linenumber

def read_samplesheet(sample_sheet_path):
	linenumber = find_column_header_linenumber(sample_sheet_path)
	df = pd.read_csv(sample_sheet_path, skiprows = linenumber, index_col = 0)
	return df

def get_index_coordinates_clash_list(sample_sheet):
	index_coordinates_clash_list = []
	for i7, i5 in list(zip(sample_sheet["I7_Index_ID"],  sample_sheet["I5_Index_ID"])):
		try:
			xcoord, ycoord = I7_LIST.index(i7), I5_LIST.index(i5)
		except:
			pass
		index_coordinates_clash_list.append((xcoord, ycoord))
	return index_coordinates_clash_list

def given_mouse_get_xy():
	x, y = pygame.mouse.get_pos()
	return x, y

def get_row_column(x, y):
	return y // (GRID_HEIGHT + MARGIN_THICKNESS), x // (GRID_WIDTH + MARGIN_THICKNESS)

def given_xy_get_rowcolumn(x, y):
	row, column = get_row_column(x, y)
	return row, column

def given_mouse_get_rowcolumn():
	row, column = given_xy_get_rowcolumn(*given_mouse_get_xy())
	return row, column

def given_mouse_get_value(grid):
	row, column = given_mouse_get_rowcolumn()
	try:
		return grid[row][column]
	except IndexError as error:
		pass
		# print("Out of bounds")

def print_indices(grid):
	for feature, mapvalue in FEATURE_MAPVALUE.items():
		item_list = np.where(grid == mapvalue)
		if len(item_list[0]) > 0:
			print(f"Getting {feature} list")
			if feature == "ALREADY CHOSEN":
				print(f"{len(item_list[0])} index combinations already chosen")
			elif feature == "WE ARE CHOOSING THIS":
				for xcoord, ycoord in list(zip(*item_list)):
					i7, i5 = I7_LIST[xcoord], I5_LIST[ycoord]
					print(i7, i5, sep = "\t")
			print()

def draw_world_grid(surface, grid):
	for row in range(NROWS):
		for column in range(NCOLS):
			COLOR_KEY = grid[row][column]
			color = COLOR_MAP[COLOR_KEY]
			pygame.draw.rect(
				surface,
				 color,
				 [(MARGIN_THICKNESS + GRID_WIDTH) * column + MARGIN_THICKNESS,
				  (MARGIN_THICKNESS + GRID_HEIGHT) * row + MARGIN_THICKNESS,
				  GRID_WIDTH,
				  GRID_HEIGHT]
			)

def draw_world_lines(surface):
	for col in range(0, NCOLS + 1, 8):
		x_pos = (MARGIN_THICKNESS + GRID_WIDTH) * col
		pygame.draw.line(
			surface,
			LINECOLOR,
			(x_pos, 0),
			(x_pos, WINDOW_HEIGHT)
		)

	for row in range(0, NROWS + 1, 8):
		y_pos = (GRID_HEIGHT + MARGIN_THICKNESS) * row
		pygame.draw.line(
			surface,
			LINECOLOR,
			(0, y_pos),
			(WINDOW_WIDTH, y_pos)
		)

def put_index_labels(surface, font):
	for i, i7 in enumerate(I7_LIST):
		textsurface = font.render(i7, True, WHITE)
		x_coord_label = (MARGIN_THICKNESS + GRID_WIDTH) * NCOLS + 3
		y_coord_label = i * (MARGIN_THICKNESS + GRID_HEIGHT)
		surface.blit(textsurface, (x_coord_label, y_coord_label))

	for i, i5 in enumerate(I5_LIST):
		textsurface = font.render(i5, True, WHITE)
		textsurface = pygame.transform.rotate(textsurface, 90)
		x_coord_label = i * (MARGIN_THICKNESS + GRID_WIDTH)
		y_coord_label = (MARGIN_THICKNESS + GRID_HEIGHT) * NROWS + 3
		surface.blit(textsurface, (x_coord_label, y_coord_label))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def choose_samplesheet_mark_used(grid):
	win = Tk()
	win.withdraw()
	filename = filedialog.askopenfilename()
	if filename =="": 
		filename = None 
	else:
		df = read_samplesheet(filename)
		for i7_coor, i5_coor in get_index_coordinates_clash_list(df):
			grid[i7_coor, i5_coor] = 100
		
	return grid


