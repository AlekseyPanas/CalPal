import pygame


class Object:
    def __init__(self, lifetime, z_order, image, pos, tags):
        # Variables for rendering
        self.sprite_image = image
        self.rect = self.sprite_image.get_rect(center=pos)
        self.pos = pos

        self.lifetime = lifetime
        self.kill = False

        # Draw order
        self.z_order = z_order

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

    def run_sprite(self, manager):
        pass

    def render(self, surface):
        pass


class GUI(Object):
    def __init__(self, lifetime, z_order, image, pos, tags):
        super().__init__(lifetime, z_order, image, pos, tags)

    def run_sprite(self, manager):
        pass

    def render(self, surface):
        pass


class Creature(Object):
    def __init__(self, lifetime, z_order, image, pos, tags):
        super().__init__(lifetime, z_order, image, pos, tags)

    def run_sprite(self, manager):
        pass

    def render(self, surface):
        pass
