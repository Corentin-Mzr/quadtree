class Vector2D:
    """
    Simple Vector class
    """
    __slots__ = ('x', 'y')

    def __init__(self,
                 x: float,
                 y: float):
        """
        Vector constructor
        :param x: Some value
        :param y: Some value
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        assert isinstance(other, Vector2D)
        return Vector2D(self.x + other.x, self.y + other.y)
    __radd__ = __add__

    def __iadd__(self, other):
        assert isinstance(other, Vector2D)
        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        assert isinstance(other, Vector2D)
        return Vector2D(self.x - other.x, self.y - other.y)
    __rsub__ = __sub__

    def __isub__(self, other):
        assert isinstance(other, Vector2D)
        self.x -= other.x
        self.y -= other.y

    def __truediv__(self, other):
        assert isinstance(other, (int, float))
        return Vector2D(self.x / other, self.y / other)

    def __itruediv__(self, other):
        assert isinstance(other, (int, float))
        self.x /= other
        self.y /= other

    def __mul__(self, other):
        assert isinstance(other, (int, float))
        return Vector2D(self.x * other, self.y * other)
    __rmul__ = __mul__

    def __imul__(self, other):
        assert isinstance(other, (int, float))
        self.x *= other
        self.y *= other

    def __str__(self):
        return f"Vector2D({self.x}, {self.y})"

    def distance(self, other) -> float:
        """
        Calculates the distance between two vectors
        """
        assert isinstance(other, Vector2D)
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
