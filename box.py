from vector2d import Vector2D
from particle import Particle

import pygame

class Box:
    """
    Simple box class for the quadtree
    """
    __slots__ = ('center', 'hdim')

    def __init__(self,
                 center: Vector2D,
                 half_dimension: Vector2D):
        """
        Box constructor
        :param center: Center of the box
        :param half_dimension: Half width and height of the box
        """
        self.center = center
        self.hdim = half_dimension

    def does_contain(self, p: Particle) -> bool:
        """
        Checks if the box contains the given point
        """
        x_bound = self.center.x - self.hdim.x <= p.position.x <= self.center.x + self.hdim.x
        y_bound = self.center.y - self.hdim.y <= p.position.y <= self.center.y + self.hdim.y

        return x_bound and y_bound

    def intersects(self, other) -> bool:
        """
        Checks if the box intersects with another box
        """
        assert isinstance(other, Box)
        self_min = self.center + Vector2D(-self.hdim.x, -self.hdim.y)
        self_max = self.center + Vector2D(self.hdim.x, self.hdim.y)

        other_min = other.center + Vector2D(-other.hdim.x, -other.hdim.y)
        other_max = other.center + Vector2D(other.hdim.x, other.hdim.y)

        # Check if a box is to the left of the other
        if self_max.x < other_min.x or other_max.x < self_min.x:
            return False

        # Check if a box is above the other
        if self_max.y < other_min.y or other_max.y < self_min.y:
            return False

        # Conditions are not met, boxes intersect
        return True

    def draw(self, screen, color: tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Draw the box on screen
        """
        rect = pygame.Rect(self.center.x - self.hdim.x, self.center.y - self.hdim.y, 2 * self.hdim.x, 2 * self.hdim.y)
        pygame.draw.rect(screen, color, rect, width=1)
