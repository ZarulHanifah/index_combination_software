import pygame
from world_constants import *
from game import Game


def setup():
	pygame.init()
	pygame.display.set_icon(pygame.image.load(LOGO_PATH))
	pygame.display.set_caption(SOFTWARE_CAPTION)

	mygame = Game()


	while mygame.running_game:

		while mygame.running_menu:
			mygame.handle_events_menu()
			mygame.draw_menu()
			pygame.display.update()

		mygame.handle_events_game()
		mygame.draw_game()
		pygame.display.update()

if __name__ == "__main__":
	setup()