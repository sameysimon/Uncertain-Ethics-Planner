from enum import Enum

class AttackResult(Enum):
    ATTACK = 1
    ABSOLUTE_ATTACK=2
    REVERSE = -1
    ABSOLUTE_REVERSE=-2
    DRAW = 0