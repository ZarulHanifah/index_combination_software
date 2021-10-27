import sys
import pygame
from index_combination.world_constants import *
import index_combination.support_functions as sf

class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_icon(pygame.image.load(LOGO_PATH))
		pygame.display.set_caption(SOFTWARE_CAPTION)

		self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
		self.bigger_font = pygame.font.SysFont('Calibri', 30)
		self.smaller_font = pygame.font.SysFont('Calibri', 15)
		self.grid = sf.initiate_grid()
		self.running_menu = True
		self.running_game = True
		self.dragging = False

		self.button_menu_samplesheet = pygame.Rect(50, 100, 200, 50)
		self.button_start_now = pygame.Rect(50, 200, 200, 50)

		while self.running_menu:
			self.handle_events_menu()
			self.draw_menu()

		while self.running_game:
			self.handle_events_game()
			self.draw_game()

	def myquit(self):
		pygame.quit()
		sys.exit()

	def handle_events_menu(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				# self.running_menu = False
				self.myquit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				mx, my = pygame.mouse.get_pos()
				
				if self.button_menu_samplesheet.collidepoint((mx, my)):
					try:
						self.grid = sf.choose_samplesheet_mark_used(self.grid)
						self.running_menu = False
					except:
						pass
				if self.button_start_now.collidepoint((mx, my)):
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
						print(f"Out of bounds:\n{error}")
					
				elif event.button == CLICK_BUTTON["MIDDLE"]:
					self.dragging = True
					try:
						pass
						# if current_value != 100:
						# 	self.grid[self.start_row][self.start_column] = 100
						# elif current_value == 100:
						# 	self.grid[self.start_row][self.start_column] = 0
					except IndexError as error:
						print(f"Out of bounds:\n{error}")
					
			elif event.type == pygame.MOUSEBUTTONUP:
				self.dragging = False
				self.end_row, self.end_column = sf.given_mouse_get_rowcolumn()
				
				try:
					row1, row2 = sorted([self.start_row, self.end_row])
					column1, column2 = sorted([self.start_column, self.end_column])
				except:
					pass
					
				if event.button == CLICK_BUTTON["LEFT"]:
					try:
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
				elif event.button == CLICK_BUTTON["MIDDLE"]:
					try:
						for row in range(row1, row2 + 1):
							for column in range(column1, column2 + 1):
								try: 
									current_value = self.grid[row][column]
									if current_value == 100:
										self.grid[row][column] = 0
									elif current_value == 10:
										self.grid[row][column] = 100
									elif current_value == 0:
										self.grid[row][column] = 100

								except IndexError as error:
									pass
								
					except:
						pass
								# print("Out of bounds")

			elif event.type == pygame.MOUSEMOTION:
				if self.dragging:
					pass

	def draw_menu(self):
		self.surface.fill(BLACK)

		sf.draw_text("SYL INDEX COMBINATION SOFTWARE", self.bigger_font, WHITE, self.surface, 20, 20)

		pygame.draw.rect(self.surface, RED, self.button_menu_samplesheet)
		pygame.draw.rect(self.surface, RED, self.button_start_now)

		sf.draw_text("READ SAMPLE SHEET", self.smaller_font, WHITE, self.surface, 55, 120)
		sf.draw_text("START NOW", self.smaller_font, WHITE, self.surface, 55, 220)

		pygame.display.flip()

	def draw_game(self):
		self.surface.fill(BLACK)
		sf.draw_world_grid(self.surface, self.grid)
		sf.draw_world_lines(self.surface)
		sf.put_index_labels(self.surface, self.smaller_font)

		pygame.display.flip()

if __name__ == "__main__":
	Game()