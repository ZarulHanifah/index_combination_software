import sys
import pygame
from world_constants import *
import support_functions as sf

class Game:
	def __init__(self):
		self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.myfont = pygame.font.SysFont('Calibri', 15)
		self.grid = sf.initiate_grid()
		self.running_menu = True
		self.running_game = True
		self.dragging = False

	def myquit(self):
		pygame.quit()
		sys.exit()

	def handle_events_menu(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running_menu = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				mx, my = pygame.mouse.get_pos()
				print(mx, my)

				if self.button_1.collidepoint((mx, my)):
					self.running_menu = False
				if self.button_2.collidepoint((mx, my)):
					self.running_menu = False

	def handle_events_game(self):
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sf.print_indices(self.grid)
				self.myquit()
				return False
			
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.start_row, self.start_column = sf.given_mouse_get_rowcolumn()
				current_value = sf.given_mouse_get_value(self.grid)
				
				if event.button == CLICK_BUTTON["LEFT"]:
					self.dragging = True
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
					try:
						self.dragging = False
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
					except:
						pass
								# print("Out of bounds")

			elif event.type == pygame.MOUSEMOTION:
				if self.dragging:
					pass

	def draw_menu(self):
		self.surface.fill(GREEN)

		sf.draw_text("main_menu", self.myfont, WHITE, self.surface, 20, 20)

		self.button_1 = pygame.Rect(50, 100, 200, 50)
		self.button_2 = pygame.Rect(50, 200, 200, 50)

		pygame.draw.rect(self.surface, RED, self.button_1)
		pygame.draw.rect(self.surface, RED, self.button_2)

	def draw_game(self):
		self.surface.fill(BLACK)
		sf.draw_world_grid(self.surface, self.grid)
		sf.draw_world_lines(self.surface)
		sf.put_index_labels(self.surface, self.myfont)