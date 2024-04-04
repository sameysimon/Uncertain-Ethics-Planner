from Raspberry.Environment.GeneralMDP import MDP
from Raspberry.Environment.Theory.Absolutism import Absolutism

class Absolute(Absolutism):
    
    def __init__(self) -> None:
        self.badTiles=[4]
        self.badActions=[]

    def JudgeTransition(self, successor:MDP.Successor):
        if successor.targetState.props['tile'] in self.badTiles:
            return True
        if successor.targetState.action in self.badActions:
            return True
        return False