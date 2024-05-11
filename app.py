import pygame
import sys

from settings import WIDTH, HEIGHT, TITLE, BG_COLOR
from quadtree import QuadTree
from box import Box
from vector2d import Vector2D
from particle import Particle

import random


class App:
    """
    Simple Application class
    """

    def __init__(self,
                 width: int = WIDTH,
                 height: int = HEIGHT,
                 title: str = TITLE,
                 bg_color: tuple[int, int, int] = BG_COLOR):
        """
        Initialize the application
        :param width: Window width
        :param height: Window height
        :param title: Window title
        :param bg_color: Background color
        """
        # Store some variables
        self.width = width
        self.height = height
        self.title = title
        self.bg_color = bg_color
        self.is_running = True

        # Setup Pygame window
        self._set_up_pygame()

        self.particles: list[Particle] = [
            Particle(random.randint(0, WIDTH),
                     random.randint(0, HEIGHT),
                     radius=4.0)
            for _ in range(500)
        ]
        self.qt = None

    def _set_up_pygame(self) -> None:
        """
        Set up Pygame
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.last_time = 0

    def handle_events(self) -> None:
        """
        Handle window events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.qt.insert(Particle(x=event.pos[0], y=event.pos[1], radius=4.0))

    def update(self, dt: float) -> None:
        self.qt = QuadTree(Box(Vector2D(self.width // 2, self.height // 2),
                               Vector2D(self.width // 2, self.height // 2)))

        for p in self.particles:
            p.move(dt)
            self.qt.insert(p)

        for p in self.particles:
            highlight = False
            others = self.qt.query_range(Box(p.position, Vector2D(2 * p.radius, 2 * p.radius)))
            for other in others:
                if p.intersects(other) and p != other:
                    highlight = True
            if highlight:
                p.set_color((255, 0, 0))
            else:
                p.set_color((255, 255, 255))

        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # self.box_range = Box(Vector2D(mouse_x, mouse_y), Vector2D(50, 50))
        # self.found = self.qt.query_range(self.box_range)

    def clear(self) -> None:
        """
        Clear screen
        """
        self.screen.fill(self.bg_color)

    def draw(self) -> None:
        """
        Draw objects on screen
        """
        for p in self.particles:
            p.draw(self.screen)

        #self.box_range.draw(self.screen, (255, 0, 0))
        self.qt.draw(self.screen)

        #for p in self.found:
        #    p.draw(self.screen, (255, 0, 0))

    def display_fps(self) -> None:
        if pygame.time.get_ticks() - self.last_time > 1000:
            pygame.display.set_caption(f"{TITLE} | FPS {self.clock.get_fps():.0f}")
            self.last_time = pygame.time.get_ticks()

    def display(self) -> None:
        """
        Display the new frame
        """
        self.display_fps()
        pygame.display.flip()

    def run(self) -> None:
        """
        Run the application
        """
        while self.is_running:
            self.handle_events()
            self.update(0.01)
            self.clear()
            self.draw()
            self.display()
            self.clock.tick()

        self.quit()

    @staticmethod
    def quit() -> None:
        """
        Quit the application and destroy objects if necessary
        """
        pygame.quit()
        sys.exit()
