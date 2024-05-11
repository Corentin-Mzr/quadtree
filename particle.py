import pygame
from vector2d import Vector2D
import random

class Particle:
    """
    Basic particle class
    """
    def __init__(self,
                 x: float = 0.0,
                 y: float = 0.0,
                 vx: float = 0.0,
                 vy: float = 0.0,
                 ax: float = 0.0,
                 ay: float = 9.81,
                 radius: float = 1.0,
                 color: tuple[int, int, int] = (255, 255, 255)):
        """
        Particle constructor
        :param x:
        :param y:
        :param vx:
        :param vy:
        :param ax:
        :param ay:
        :param radius:
        :param color:
        """
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(vx, vy)
        self.acceleration = Vector2D(ax, ay)

        self.color = color
        self.radius = radius

    def move(self, dt: float) -> None:
        """
        Move the particle with Velocity Verlet integration
        :param dt: Delta time
        """
        self.position = self.position + Vector2D(random.randint(-3, 3), random.randint(-3, 3)) * 2 * dt
        #self.position = self.position + self.velocity * dt + 0.5 * self.acceleration * dt ** 2
        #self.velocity = self.velocity + 0.5 * self.acceleration * dt

    def apply_force(self, force: Vector2D) -> None:
        """
        Apply a force on the particle
        """
        self.acceleration += force

    def handle_bounds(self, wmin: float, wmax: float, hmin: float, hmax: float) -> None:
        """
        Handle bounds
        :param wmin:
        :param wmax:
        :param hmin:
        :param hmax:
        """
        self.position.x = min(max(wmin, self.position.x), wmax)
        self.position.y = min(max(hmin, self.position.y), hmax)

    def intersects(self, other) -> bool:
        """
        Check if two particles intersect
        """
        assert isinstance(other, Particle)
        return self.position.distance(other.position) <= self.radius + other.radius

    def set_color(self, color: tuple[int, int, int]) -> None:
        self.color = color

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the particle on screen
        """
        pygame.draw.circle(screen,
                           self.color,
                           (self.position.x, self.position.y),
                           radius=self.radius)
