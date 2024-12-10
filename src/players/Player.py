
from src.units.Team import Team

class Player(Team):
    """
    Players in the game use this object. Inherits from team.
    Does not need the same functions that Computer needs, left here for future compatibility
    """
    def __init__(self):
        super().__init__()


