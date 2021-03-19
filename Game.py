import pygame
import Constants
import Renderer
import Object
import Utils
import time


class Manager:
    def __init__(self):
        # Screen window
        self.screen = pygame.display.set_mode(Constants.SCREEN_SIZE, pygame.DOUBLEBUF)
        self.running = True

        # All the game objects
        self.background_image = pygame.Surface(Constants.SCREEN_SIZE)
        self.background_image.fill((150, 150, 150))
        self.game_objects = []
        self.game_object_add_queue = []
        self.game_object_delete_queue = []

        # Adds starting objects
        self.add_object(Object.GUI(None, 999, [i/2 for i in Constants.SCREEN_SIZE]))
        self.add_object(Object.Grass(None, 1, (200, 200)))
        self.add_object(Object.Snack(None, 2, (300, 400)))
        self.add_object(Object.Kibble(None, 3, (250, 250)))
        self.update_objects()

        # Game events
        self.events = []

        # Time
        self.clock = pygame.time.Clock()
        self.fps = 0
        self.last_fps_show = 0
        self.ticks_last_frame = pygame.time.get_ticks()

        # Class instances
        self.renderer = Renderer.Renderer()

    def add_object(self, obj):
        self.game_object_add_queue.append(obj)

    def update_objects(self):
        # Checks queue
        if len(self.game_object_add_queue):

            # Add queued objects
            for obj in self.game_object_add_queue:
                self.game_objects.append(obj)

            # Sort list for rendering
            self.game_objects.sort(key=lambda i: i.z_order)

            # Clear queue
            self.game_object_add_queue = []

        # Manage object life
        for obj in self.game_objects:
            obj.exist_time += 1
            if obj.lifetime is not None:
                obj.lifetime -= 1
            if (obj.lifetime is not None and obj.lifetime <= 0) or obj.kill:
                self.game_object_delete_queue.append(obj)

        # Deletes queued objects and clears delete queue
        for obj in self.game_object_delete_queue:
            if obj in self.game_objects:
                self.game_objects.remove(obj)
        self.game_object_delete_queue = []

    def start_game(self):
        while self.running:

            # Updates time delta
            t = pygame.time.get_ticks()
            # deltaTime in seconds.
            deltaTime = (t - self.ticks_last_frame) / 1000.0
            self.ticks_last_frame = t

            # Clears screen
            self.screen.fill((0, 0, 0))

            # Gets events
            self.events = pygame.event.get()
            # Closes game on quit
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

            # Run objects
            for obj in self.game_objects:
                obj.run_sprite(self, deltaTime)

            # Render
            self.renderer.render(self, self.screen, deltaTime)

            # Updates objects (adds new, delete old)
            self.update_objects()

            # Updates display
            pygame.display.update()

            # sets fps to a variable. can be set to caption any time for testing.
            self.last_fps_show += 1
            if self.last_fps_show == 30:  # every 30th frame:
                self.fps = self.clock.get_fps()
                pygame.display.set_caption("CalPal v1.0" + "   FPS: " + str(self.fps))
                self.last_fps_show = 0

            # fps max 60
            self.clock.tick(120)

    @staticmethod
    def load_image(path, size=None):
        img = pygame.image.load(path)
        if size is not None:
            img = pygame.transform.smoothscale(img, size)
        return img.convert_alpha()
