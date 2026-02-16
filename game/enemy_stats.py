
class EnemyStats:
    H0 = 2.155
    rH = 1.08994

    A0 = 1.069
    rA = 1.10263

    S0 = 0.998
    rS = 1.00079

    def __init__(self):
        self.health = EnemyStats.H0
        self.attack = EnemyStats.A0

    def update_health(self, wave: int):
        self.health += EnemyStats.H0 * (EnemyStats.rH ** (wave - 1) * (EnemyStats.rH - 1))

    def update_attack(self, wave: int):
        self.attack += EnemyStats.A0 * (EnemyStats.rA ** (wave - 1) * (EnemyStats.rA - 1))
    
    def speed(self, wave: int) -> float:
        return EnemyStats.S0 * (EnemyStats.rS ** (wave))
