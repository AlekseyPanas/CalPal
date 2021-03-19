import pygame
import Constants
import Renderer
import Object


class Manager:
    def __init__(self):
        # Screen window
        self.screen = pygame.display.set_mode(Constants.SCREEN_SIZE)
        self.running = True

        # All the game objects
        self.game_objects = []

        # Game events
        self.events = []

        # Class instances
        self.renderer = Renderer.Renderer()

    def start_game(self):
        while self.running:
            # Gets events
            self.events = pygame.event.get()

            # Run objects
            for obj in self.game_objects:
                obj.run_sprite(self)

            # Render
            self.renderer.render(self)
