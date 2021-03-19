import pygame


class Renderer:
    def __init__(self):
        pass

    def render(self, manager, screen, time_delta):
        # Draws background
        screen.blit(manager.background_image, (0, 0))

        # Renders objects
        for obj in manager.game_objects:
            if obj.do_render:
                obj.render(screen, time_delta)
