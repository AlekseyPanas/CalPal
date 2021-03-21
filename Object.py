import random
import pygame
import Utils
pygame.font.init()


class Object:
    def __init__(self, lifetime, z_order, image, center_pos, tags=(), physics_rect=None, physics_rect_offset=(0, 0)):
        # Variables for rendering
        self.sprite_surface = image
        self.image_rect = self.sprite_surface.get_rect(center=center_pos)
        self.center = center_pos

        # Physics Descriptors
        self.physics_rect = physics_rect if physics_rect is not None else self.image_rect
        self.physics_rect.center = (center_pos[0] + physics_rect_offset[0],
                                    center_pos[1] + physics_rect_offset[1])
        self.physics_rect_offset = physics_rect_offset

        # Life determination
        self.lifetime = lifetime
        self.kill = False

        # Render this object?
        self.do_render = True

        # Is this object solid (can it be walked through)
        self.is_collidable = False

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
        self.pre_update(manager, time_delta)

        # Updates the centers of the physics and image rectangles
        self.update_rects()

        self.post_update(manager, time_delta)

    def update_rects(self):
        self.physics_rect.center = (self.center[0] + self.physics_rect_offset[0],
                                    self.center[1] + self.physics_rect_offset[1])
        self.image_rect.center = self.center

    def pre_update(self, manager, time_delta):
        pass

    def post_update(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        pass









class GUI(Object):
    def __init__(self, lifetime, z_order, pos, tags=()):
        super().__init__(lifetime, z_order, pygame.Surface(Utils.cscale(600, 500)), pos, tags)

        self.tags.add("gui")

        self.calories = 2000

        self.font = pygame.font.SysFont("Arial", Utils.cscale(30))

    def pre_update(self, manager, time_delta):
        for event in manager.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and self.calories >= 100:
                    manager.add_object(Grass(None, pygame.mouse.get_pos()))
                    self.calories -= 100
                elif event.key == pygame.K_2 and self.calories >= 200:
                    manager.add_object(Kibble(None, pygame.mouse.get_pos()))
                    self.calories -= 200
                elif event.key == pygame.K_3 and self.calories >= 300:
                    manager.add_object(Snack(None, pygame.mouse.get_pos()))
                    self.calories -= 300
                if event.key == pygame.K_e and self.calories >= 10:
                    self.calories -= 10

    def render(self, surface, time_delta):
        surface.blit(self.font.render("Calories " + str(self.calories), True, (200, 0, 0)), Utils.cscale(100, 50))









class Creature(Object):
    MAXSPEED = 1
    MAXFORCE = 0.25

    def __init__(self, lifetime, pos, tags=()):
        super().__init__(lifetime, 5, Utils.load_image("assets/images/Buster_Happy.png", (200, 150)), pos, tags)

        self.tags.add("creature")
        """self.skeleton = Skeleton.Skeleton((
            Skeleton.Bone(start_node_pos=(-100, 100),
                          end_node_pos=(100, 0)),
            Skeleton.Bone(start_node_pos=(0, 0),
                          end_node_pos=(150, 0)),
        ))
        self.skeleton.bones[0].add_connection(Skeleton.Bone.NodeTypes.END_NODE,
                                              self.skeleton.bones[1],
                                              Skeleton.Bone.NodeTypes.START_NODE)
        """
        self.sprite_surface_right = pygame.transform.flip(self.sprite_surface, True, False).convert_alpha()

        self.pos = self.center
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.happiness = 100
        self.hunger = 100
        self.thirst = 100
        self.moving = False
        self.food = None

    def go_to(self, manager, target, time_delta):
        self.applyForce(self.seek(target))
        obstacles = [obj for obj in manager.game_objects if obj.is_collidable]
        if "pond" in self.food.tags:
            obstacles = [obj for obj in obstacles if "pond" not in self.food.tags]
        for obstacle in obstacles:
            self.applyForce(self.avoid(obstacle.center))
        self.vel[0] += self.acc[0] * time_delta * 100
        self.vel[1] += self.acc[1] * time_delta * 100
        self.pos[0] += self.vel[0] * time_delta * 100
        self.pos[1] += self.vel[1] * time_delta * 100
        self.acc = [0, 0]

    def seek(self, target):
        desired = (target[0] - self.pos[0], target[1] - self.pos[1])
        dist = (desired[0] ** 2 + desired[1] ** 2) ** (1 / 2)
        speed = Creature.MAXSPEED
        if dist < 100:
            speed = dist / 100
        desired = (desired[0] * speed / dist, desired[1] * speed / dist)
        steer = (desired[0] - self.vel[0], desired[1] - self.vel[1])
        mag = (steer[0] ** 2 + steer[1] ** 2) ** (1 / 2)
        if mag > Creature.MAXFORCE:
            steer = (steer[0] * Creature.MAXFORCE / mag, desired[1] * Creature.MAXFORCE / mag)
        if dist < 10:
            self.moving = False
            self.vel = [0, 0]
            return 0, 0
        else:
            return steer

    def avoid(self, obstacle):
        desired = (obstacle[0] - self.pos[0], obstacle[1] - self.pos[1])
        dist = (desired[0] ** 2 + desired[1] ** 2) ** (1 / 2)
        if dist < 200:
            desired = (-desired[0] * Creature.MAXSPEED / dist, -desired[1] * Creature.MAXSPEED / dist)
            steer = (desired[0] - self.vel[0], desired[1] - self.vel[1])
            # mag = (steer[0] ** 2 + steer[1] ** 2) ** (1 / 2)
            # if mag > Creature.MAXFORCE:
            #     steer = (steer[0] * 2 * Creature.MAXFORCE / mag, desired[1] * 2 * Creature.MAXFORCE / mag)
            return steer
        else:
            return 0, 0

    def applyForce(self, force):
        self.acc[0] += force[0]
        self.acc[1] += force[1]

        self.tags.add("creature")

    def pre_update(self, manager, time_delta):
        if not self.moving:
            if random.randint(0, 1) == 0:
                self.hunger -= time_delta * random.randint(1, 10)
            else:
                self.thirst -= time_delta * random.randint(1, 10)
        print(self.hunger, self.thirst)
        if self.hunger <= 0 or self.thirst <= 0:
            # Die
            return
        if self.moving:
            self.go_to(manager, self.food.center, time_delta)
        else:
            if self.food is not None:
                if "pond" in self.food.tags:
                    self.update_thirst(100)
                else:
                    self.update_hunger(self.food.calories)
                    self.food.kill = True
                    self.food = None
            if self.thirst / self.hunger > 2 or self.hunger <= random.randint(25, 50):
                self.food = random.choice([obj for obj in manager.game_objects if "food" in obj.tags])
                self.moving = True
            if self.hunger / self.thirst > 2 or self.thirst <= random.randint(25, 50):
                self.food = [obj for obj in manager.game_objects if "pond" in obj.tags][0]
                self.moving = True

    def post_update(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        # self.skeleton.render(surface, time_delta, self.center)
        # pygame.draw.circle(surface, (255, 200, 0), self.center, 5)

        #pygame.draw.rect(surface, (255, 0, 0), self.physics_rect, 1)
        surface.blit(self.sprite_surface if self.vel[0] < 0 else self.sprite_surface_right, self.image_rect)

    def update_hunger(self, hunger):
        self.hunger = min(max(self.hunger + hunger ** (1 / 2), 0), 100)

    def update_thirst(self, thirst):
        self.thirst = min(max(self.thirst + thirst ** (1 / 2), 0), 100)









class Grass(Object):
    SEED2SPROUT_TIME = 3600
    SPROUT2GRASS_TIME = 15000
    SEED2SPROUT_TIME = 100
    SPROUT2GRASS_TIME = 200

    STAGES = {0: "seed", 1: "sprout", 2: "grass"}
    STAGE2IDX = {"seed": 0, "sprout": 1, "grass": 2}
    STAGE2CAL = {STAGES[0]: 10, STAGES[1]: 100, STAGES[2]: 250}

    def __init__(self, lifetime, pos, tags=()):
        super().__init__(lifetime, 1, pygame.Surface(Utils.cscale(70, 45)), pos, tags)

        # Grass has 3 stages of grass
        self.sprite_surface = [Utils.load_image("assets/images/grass_0.png", Utils.cscale(70, 45)),
                               Utils.load_image("assets/images/grass_1.png", Utils.cscale(70, 45)),
                               Utils.load_image("assets/images/grass_2.png", Utils.cscale(70, 45))]

        self.tags.add("grass")
        self.tags.add("food")

        # Growth Stage
        self.stage = Grass.STAGES[0]

        # Universal variables for all foods
        self.calories = self.STAGE2CAL[self.stage]
        self.happiness_index = 5  # Scale that goes from 0-100, where 100 is the most enjoyable food

    def pre_update(self, manager, time_delta):
        # Updates grass growth stages and calories
        if self.exist_time >= Grass.SEED2SPROUT_TIME and self.stage == Grass.STAGES[0]:
            self.stage = Grass.STAGES[1]
            self.calories = self.STAGE2CAL[self.stage]
        if self.exist_time >= Grass.SPROUT2GRASS_TIME and self.stage == Grass.STAGES[1]:
            self.stage = Grass.STAGES[2]
            self.calories = self.STAGE2CAL[self.stage]

    def post_update(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        surface.blit(self.sprite_surface[Grass.STAGE2IDX[self.stage]], self.image_rect)
        #pygame.draw.rect(surface, (255, 0, 0), self.physics_rect, 1)









class Kibble(Object):
    def __init__(self, lifetime, pos, tags=()):
        super().__init__(lifetime, 2, Utils.load_image("assets/images/kibble.png", Utils.cscale(57, 30)), pos, tags)

        self.tags.add("kibble")
        self.tags.add("food")

        # Universal variables for all foods
        self.calories = 600
        self.happiness_index = 45  # Scale that goes from 0-100, where 100 is the most enjoyable food

    def pre_update(self, manager, time_delta):
        pass

    def post_update(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        surface.blit(self.sprite_surface, self.image_rect)
        #pygame.draw.rect(surface, (255, 0, 0), self.physics_rect, 1)


class Snack(Object):
    def __init__(self, lifetime, pos, tags=()):
        super().__init__(lifetime, 3, Utils.load_image("assets/images/bone.png", Utils.cscale(65, 30)), pos, tags)

        self.tags.add("snack")
        self.tags.add("food")

        # Universal variables for all foods
        self.calories = 600
        self.happiness_index = 100  # Scale that goes from 0-100, where 100 is the most enjoyable food

    def pre_update(self, manager, time_delta):
        pass

    def post_update(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        surface.blit(self.sprite_surface, self.image_rect)
        #pygame.draw.rect(surface, (255, 0, 0), self.physics_rect, 1)









class Shack(Object):
    def __init__(self, lifetime, pos, tags=()):
        super().__init__(lifetime, 0, Utils.load_image("assets/images/shack.png", Utils.cscale(250, 250)), pos, tags)

        self.tags.add("shack")
        self.is_collidable = True

    def pre_update(self, manager, time_delta):
        pass

    def post_update(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        surface.blit(self.sprite_surface, self.image_rect)
        #pygame.draw.rect(surface, (255, 0, 0), self.physics_rect, 1)








class Pond(Object):
    ANIMATION_SPEED = 50

    def __init__(self, lifetime, pos, tags=()):
        surf = pygame.Surface(Utils.cscale(200, 150))
        surf.fill((20, 130, 200))
        super().__init__(lifetime, -1, Utils.load_image("assets/images/pond.png", Utils.cscale(260, 150)), pos, tags)

        self.ripple_images = [Utils.load_image("assets/images/ripples_1.png", Utils.cscale(260, 150)),
                              Utils.load_image("assets/images/ripples_2.png", Utils.cscale(260, 150))]
        self.ripple_idx = 0

        self.tags.add("pond")
        self.is_collidable = True

    def pre_update(self, manager, time_delta):
        pass

    def post_update(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        surface.blit(self.sprite_surface, self.image_rect)
        surface.blit(self.ripple_images[self.ripple_idx], self.image_rect)

        # Runs animation
        if self.exist_time % Pond.ANIMATION_SPEED == 0:
            self.ripple_idx = 0 if self.ripple_idx == 1 else 1

        #pygame.draw.rect(surface, (255, 0, 0), self.physics_rect, 1)
