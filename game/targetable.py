from abc import ABC, abstractmethod
import pygame


class Targetable(ABC):
    """
    Abstract base class for objects that can be targeted and take damage.
    Anything that can be a projectile target must implement this interface.
    """

    # Required attributes
    x: float
    y: float
    rect: pygame.Rect
    dead: bool

    @abstractmethod
    def take_damage(self, amount: float) -> None:
        """Apply damage to this targetable object."""
        pass
