import pygame

from vector2d import Vector2D
from box import Box
from particle import Particle


class QuadTree:
    """
    Basic Quadtree class
    """
    __slots__ = ('capacity', 'boundary', 'points', 'is_divided', 'northwest', 'northeast', 'southwest', 'southeast')

    def __init__(self, boundary: Box):
        """
        QuadTree constructor
        """
        # Number of elements the QuadTree can store
        self.capacity: int = 4

        # Boundary box of the QuadTree
        self.boundary: Box = boundary

        # Points contained in the node
        self.points: list[Particle] = []

        # Children
        self.is_divided: bool = False
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def insert(self, p: Particle) -> bool:
        """
        Insert a point into the box
        """
        # Ignore objects that don't belong to the QuadTree
        if not self.boundary.does_contain(p):
            return False

        # Check if there is enough place to insert the object
        if len(self.points) < self.capacity:
            self.points.append(p)
            return True
        else:
            # Subdivide the space and put it in one of the nodes
            if not self.is_divided:
                self.subdivide()

            if self.northwest.insert(p):
                return True
            if self.northeast.insert(p):
                return True
            if self.southwest.insert(p):
                return True
            if self.southeast.insert(p):
                return True

        return False

    def subdivide(self) -> None:
        """
        Subdivide the QuadTree into four new children
        """
        center = self.boundary.center
        hdim = self.boundary.hdim

        box_dim = hdim / 2

        nw_center = center + Vector2D(-hdim.x / 2, -hdim.y / 2)
        nw_box = Box(nw_center, box_dim)
        self.northwest = QuadTree(nw_box)

        ne_center = center + Vector2D(hdim.x / 2, -hdim.y / 2)
        ne_box = Box(ne_center, box_dim)
        self.northeast = QuadTree(ne_box)

        sw_center = center + Vector2D(-hdim.x / 2, hdim.y / 2)
        sw_box = Box(sw_center, box_dim)
        self.southwest = QuadTree(sw_box)

        se_center = center + Vector2D(hdim.x / 2, hdim.y / 2)
        se_box = Box(se_center, box_dim)
        self.southeast = QuadTree(se_box)

        self.is_divided = True

    def query_range(self, box: Box) -> list[Particle]:
        """
        Find all points in the given range
        """
        points_in_range: list[Particle] = []

        # Interrupt if the research zone does not intersect the quad
        # Returns an empty array
        if not self.boundary.intersects(box):
            return points_in_range

        # Check objects in the quad
        for p in self.points:
            if box.does_contain(p):
                points_in_range.append(p)

        # Stop if no children
        if not self.is_divided:
            return points_in_range

        # Else do the research on children
        points_in_range += self.northwest.query_range(box)
        points_in_range += self.northeast.query_range(box)
        points_in_range += self.southwest.query_range(box)
        points_in_range += self.southeast.query_range(box)

        return points_in_range

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the quadtree and particles on screen
        """
        self.boundary.draw(screen)

        if self.is_divided:
            self.northwest.draw(screen)
            self.northeast.draw(screen)
            self.southwest.draw(screen)
            self.southeast.draw(screen)

        for point in self.points:
            point.draw(screen)
