import pygame


class Object:
    def __init__(self, lifetime, z_order, image, center_pos, tags):
        # Variables for rendering
        self.sprite_surface = image
        self.rect = self.sprite_surface.get_rect(center=center_pos)
        self.center = center_pos

        # Life determination
        self.lifetime = lifetime
        self.kill = False

        # Render this object?
        self.do_render = True

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

    def run_sprite(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        pass


class GUI(Object):
    def __init__(self, lifetime, z_order, image, pos, tags):
        super().__init__(lifetime, z_order, image, pos, tags)

    def run_sprite(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        pass


class Creature(Object):
    def __init__(self, lifetime, z_order, image, pos, tags):
        super().__init__(lifetime, z_order, image, pos, tags)

    def run_sprite(self, manager, time_delta):
        pass

    def render(self, surface, time_delta):
        pass
