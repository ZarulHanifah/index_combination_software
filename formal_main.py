import sys
import pygame
import numpy as np
import pandas as pd
from world_constants import *
import support_functions as sf
import subprocess


class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_icon(pygame.image.load(LOGO_PATH))
		pygame.display.set_caption(SOFTWARE_CAPTION)

		self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.myfont = pygame.font.SysFont('Calibri', 15)
		self.grid = sf.initiate_grid()
		self.running = True
		self.draging = False

		self.surface.fill(BLACK)

	def myquit(self):
		pygame.quit()
		# sys.exit()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sf.print_indices(self.grid)
				self.myquit()
				return False
			
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.start_row, self.start_column = sf.given_mouse_get_rowcolumn()
				current_value = sf.given_mouse_get_value(self.grid)
				
				if event.button == CLICK_BUTTON["LEFT"]:
					self.draging = True
					try:
						pass
					except IndexError as error:
						print("Out of bounds")
					
				if event.button == CLICK_BUTTON["MIDDLE"]:
					try:
						if current_value != 100:
							self.grid[self.start_row][self.start_column] = 100
						elif current_value == 100:
							self.grid[self.start_row][self.start_column] = 0
					except:
						pass
					
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == CLICK_BUTTON["LEFT"]:
					self.draging = False
					self.end_row, self.end_column = sf.given_mouse_get_rowcolumn()
					
					row1, row2 = sorted([self.start_row, self.end_row])
					column1, column2 = sorted([self.start_column, self.end_column])

					for row in range(row1, row2 + 1):
						for column in range(column1, column2 + 1):
							try: 
								current_value = self.grid[row][column]
								if current_value == 100:
									pass
								elif current_value == 10:
									self.grid[row][column] = 0
								elif current_value == 0:
									self.grid[row][column] = 10

							except IndexError as error:
								pass
								# print("Out of bounds")

			elif event.type == pygame.MOUSEMOTION:
				if self.draging:
					pass

	def draw_world(self):
		sf.draw_world_grid(self.surface, self.grid)
		sf.draw_world_lines(self.surface)
		sf.put_index_labels(self.surface, self.myfont)

def setup():
	mygame = Game()

	while True:
		mygame.handle_events()
		mygame.draw_world()
		pygame.display.update()

if __name__ == "__main__":
	setup()