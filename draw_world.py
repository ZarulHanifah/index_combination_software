#!/home/ahbui/Zarul/Software/anaconda3/envs/pygame/bin/python

import pygame

import numpy as np
import pandas as pd
from world_constants import *
import support_functions as sf
import subprocess

sample_sheet_path = "input_folder/M290.csv"

world_grid = sf.initiate_grid()

pygame.init()
pygame.display.set_caption(SOFTWARE_CAPTION)
pygame.font.init()

screen = pygame.display.set_mode(WINDOW_SIZE)

sample_sheet = sf.read_samplesheet(sample_sheet_path)
index_clash_list = sf.get_index_clash_list(sample_sheet)

for xcoord, ycoord in index_clash_list:
	world_grid[xcoord][ycoord] = 100

def game_loop(surface, grid):
	running = True
	clock = pygame.time.Clock()
	draging = False

	while running:
		for event in pygame.event.get():  # User did something
			
			if event.type == pygame.QUIT:
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

				running = False
			
			elif event.type == pygame.MOUSEBUTTONDOWN:
				pos_x, pos_y = pygame.mouse.get_pos()
				start_row, start_column = sf.get_row_column(pos_x, pos_y)
				current_value = grid[start_row][start_column]
				if event.button == CLICK_BUTTON["LEFT"]:
					draging = True
					

				if event.button == CLICK_BUTTON["MIDDLE"]:
					try:
						if current_value != 100:
							grid[start_row][start_column] = 100
						elif current_value == 100:
							grid[start_row][start_column] = 0
					except:
						pass
					
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == CLICK_BUTTON["LEFT"]:
					end_pos_x, end_pos_y = pygame.mouse.get_pos()
					end_row, end_column = sf.get_row_column(end_pos_x, end_pos_y)
					
					row1, row2 = sorted([start_row, end_row])
					column1, column2 = sorted([start_column, end_column])

					for row in range(row1, row2 + 1):
						for column in range(column1, column2 + 1):
							try: 
								# i7, i5 = I7_LIST[row], I5_LIST[column]
								current_value = grid[row][column]
								if current_value == 100:
									pass
								elif current_value == 10:
									grid[row][column] = 0
								elif current_value == 0:
									grid[row][column] = 10

							except IndexError as error:
								print("Out of bounds")
					draging = False

			elif event.type == pygame.MOUSEMOTION:
				if draging:
					pass
					
		surface.fill(BLACK)
	 
		sf.draw_grid(surface, grid)
		sf.draw_lines(surface)
		sf.put_index_labels(surface)
		

		clock.tick(60)
		pygame.display.flip()

	pygame.quit()

def main():
	print("_____BEGIN_____")
	game_loop(screen, world_grid)
	print("_____ENDED_____")
if __name__ == "__main__":
	main()