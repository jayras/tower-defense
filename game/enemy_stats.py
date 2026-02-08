
class BasicStats:
    @staticmethod
    def chance(wave: int) -> float:
        if wave < 3:
            return 0.95
        elif wave < 10:
            return 0.93
        elif wave < 20:
            return 0.89
        elif wave < 40:
            return 0.85
        elif wave < 100:
            return 0.82
        else:
            return 0.74

    @staticmethod
    def health(wave: int) -> float:
        # Unified exponential curve (Wave 1 → 111+)
        return 2.826 * (1.0839 ** wave)

    @staticmethod
    def attack(wave: int) -> float:
        # Unified ratio
        return 0.09 * BasicStats.health(wave)

    @staticmethod
    def speed(wave: int) -> float:
        if wave < 10:
            return 1.00
        elif wave < 20:
            return 1.01
        elif wave < 40:
            return 1.02
        elif wave < 100:
            return 1.03
        else:
            return 1.08

    @staticmethod
    def mass(wave: int) -> float:
        return 1.05