from __future__ import annotations

import math


class Vector2(object):
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self) -> Vector2:
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        else:
            return Vector2(self.x / mag, self.y / mag)
        
    def add(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)
    
    def subtract(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)
    
    def scale(self, scalar: float) -> Vector2:
        return Vector2(self.x * scalar, self.y * scalar)
    
    def round(self) -> Vector2:
        return Vector2(round(self.x), round(self.y))
    
    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
    