import random

import pygame
import Constants
import Utils


class Object:
    def __init__(self, lifetime, z_order, image, center_pos, tags=(), physics_rect=None):
        # Variables for rendering
        self.sprite_surface = image
        self.image_rect = self.sprite_surface.get_rect(center=center_pos)
        self.center = center_pos

        # Physics Descriptors
        self.physics_rect = physics_rect if physics_rect is not None else self.image_rect
        self.physics_rect.center = center_pos

        # Life determination
        self.lifetime = lifetime
        self.kill = False

        # Render this object?
        self.do_render = True

        # Draw order
        self.z_order = z_order

        # Time the object has existed
        self.exist_time = 0

        # Set of string tags that can identify an object
        self.tags = set(tags)

    @staticmethod
    def rotate(image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

    def run_sprite(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        pass


class GUI(Object):
    def __init__(self, lifetime, z_order, pos, tags=()):
        super().__init__(lifetime, z_order, pygame.Surface(Utils.cscale(600, 500)), pos, tags)

        self.tags.add("gui")

    def run_sprite(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        pass


class Creature(Object):
    def __init__(self, lifetime, z_order, image, pos, tags=()):
        super().__init__(lifetime, z_order, image, pos, tags)
        self.vel = (0, 0)
        self.acc = (0, 0)
        self.maxspeed = 10
        self.maxforce = 1
        self.happiness = 100
        self.hunger = 100
        self.thirst = 100

    def update(self):
        if self.hunger <= 0 or self.thirst <= 0:
            # Die
            return
        if self.hunger / self.thirst > 2 or self.hunger <= random.randint(25, 75):
            # look for food
            food_list = []
            self.go_to(random.choice(food_list))
            return
        if self.thirst / self.hunger > 2 or self.thirst <= random.randint(25, 75):
            # look for pond
            pond = None
            self.go_to(pond)
            return

    def go_to(self, target):
        self.applyForce(self.seek(target))
        obstacles = []
        for obstacle in obstacles:
            self.applyForce(self.avoid(obstacle))
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.acc = [0, 0]

    def seek(self, target):
        desired = (target[0] - self.pos[0], target[1] - self.pos[1])
        dist = (desired[0] ** 2 + desired[1] ** 2) ** (1 / 2)
        speed = self.maxspeed
        if dist < 100:
            speed = dist / 10
        desired = (desired[0] * speed / dist, desired[1] * speed / dist)
        steer = (desired[0] - self.vel[0], desired[1] - self.vel[1])
        mag = (steer[0] ** 2 + steer[1] ** 2) ** (1 / 2)
        if mag > self.maxforce:
            steer = (steer[0] * self.maxforce / mag, desired[1] * self.maxforce / mag)
        return steer

    def avoid(self, obstacle):
        desired = (obstacle[0] - self.pos[0], obstacle[1] - self.pos[1])
        dist = (desired[0] ** 2 + desired[1] ** 2) ** (1 / 2)
        if dist < 50:
            desired = (-desired[0] * self.maxspeed / dist, -desired[1] * self.maxspeed / dist)
            steer = (desired[0] - self.vel[0], desired[1] - self.vel[1])
            mag = (steer[0] ** 2 + steer[1] ** 2) ** (1 / 2)
            if mag > self.maxforce:
                steer = (steer[0] * self.maxforce / mag, desired[1] * self.maxforce / mag)
            return steer
        else:
            return 0, 0

    def applyForce(self, force):
        self.acc[0] += force[0]
        self.acc[1] += force[1]

        self.tags.add("creature")

    def run_sprite(self, manager, time_delta):
        self.physics_rect.center = self.center
        self.image_rect.center = self.center

    def render(self, surface, time_delta):
        pass


class Grass(Object):
    SEED2SPROUT_TIME = 3600
    SPROUT2GRASS_TIME = 15000

    STAGES = {0: "seed", 1: "sprout", 2: "grass"}
    STAGE2CAL = {STAGES[0]: 10, STAGES[1]: 100, STAGES[2]: 250}

    def __init__(self, lifetime, z_order, pos, tags=()):
        surf = pygame.Surface(Utils.cscale(100, 50))
        surf.fill((0, 200, 0))
        super().__init__(lifetime, z_order, surf, pos, tags)

        self.tags.add("grass")
        self.tags.add("food")

        # Growth Stage
        self.stage = self.STAGES[0]

        # Universal variables for all foods
        self.calories = self.STAGE2CAL[self.stage]
        self.happiness_index = 5  # Scale that goes from 0-100, where 100 is the most enjoyable food

    def run_sprite(self, manager, time_delta):
        self.physics_rect.center = self.center
        self.image_rect.center = self.center

    def render(self, surface, time_delta):
        surface.blit(self.sprite_surface, self.image_rect)


class Kibble(Object):
    def __init__(self, lifetime, z_order, pos, tags=()):
        surf = pygame.Surface(Utils.cscale(100, 85))
        surf.fill((180, 90, 0))
        super().__init__(lifetime, z_order, surf, pos, tags)

        self.tags.add("kibble")
        self.tags.add("food")

        # Universal variables for all foods
        self.calories = 600
        self.happiness_index = 45  # Scale that goes from 0-100, where 100 is the most enjoyable food

    def run_sprite(self, manager, time_delta):
        self.physics_rect.center = self.center
        self.image_rect.center = self.center

    def render(self, surface, time_delta):
        surface.blit(self.sprite_surface, self.image_rect)


class Snack(Object):
    def __init__(self, lifetime, z_order, pos, tags=()):
        surf = pygame.Surface(Utils.cscale(60, 60))
        surf.fill((200, 0, 0))
        super().__init__(lifetime, z_order, surf, pos, tags)

        self.tags.add("Snack")
        self.tags.add("food")

        # Universal variables for all foods
        self.calories = 600
        self.happiness_index = 100  # Scale that goes from 0-100, where 100 is the most enjoyable food

    def run_sprite(self, manager, time_delta):
        self.physics_rect.center = self.center
        self.image_rect.center = self.center

    def render(self, surface, time_delta):
        surface.blit(self.sprite_surface, self.image_rect)
