from abc import ABC, abstractmethod

class EnemyType(ABC):
    """
    Abstract base class for enemy types. Each enemy type has a name and stats.
    """

    # Required attributes
    name: str
    
    mass: float
    size: int
    color: tuple

    # Multipliers for enemy type.
    health_multiplier: float
    attack_multiplier: float
    speed_multiplier: float

    # Currencies for enemy type.
    gold: int
    tokens: int

    def get_gold(self, wave_number: int):
        return min(EnemyType.gold * (wave_number // 10), EnemyType.gold)
    
    def get_tokens(self, wave_number: int):
        return min(EnemyType.tokens * (wave_number // 10), EnemyType.tokens)


class BasicEnemy(EnemyType):
    name = "Basic Enemy"
    mass = 1.05
    size = 10
    color = (255, 0, 0)  # Red
    health_multiplier = 1.0
    attack_multiplier = 1.0
    speed_multiplier = 1.0
    gold = 1
    tokens = 0

class FastEnemy(EnemyType):
    name = "Fast Enemy"
    mass = BasicEnemy.mass
    size = BasicEnemy.size
    color = (255, 255, 0)  # Yellow
    health_multiplier = 1.0
    attack_multiplier = 1.0
    speed_multiplier = 2.1
    gold = 2
    tokens = 1

class TankEnemy(EnemyType):
    name = "Tank Enemy"
    mass = 5.1
    size = 20
    color = (255, 140, 0)  # Orange
    health_multiplier = 5.0
    attack_multiplier = 1.0
    speed_multiplier = 0.6
    gold = 4
    tokens = 3

class RangedEnemy(EnemyType):
    name = "Ranged Enemy"
    mass = BasicEnemy.mass
    size = BasicEnemy.size
    color = (0, 255, 255)  # Cyan
    health_multiplier = 1.0
    attack_multiplier = 1.0
    speed_multiplier = 1.0
    gold = 2
    tokens = 1

class BossEnemy(EnemyType):
    name = "Boss Enemy"
    mass = 13.0
    size = 30
    color = (128, 0, 128)  # Purple
    health_multiplier = 20.0
    attack_multiplier = 1.0
    speed_multiplier = 0.4
    gold = 10
    tokens = 5
