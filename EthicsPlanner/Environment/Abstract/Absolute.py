from EthicsPlanner.Environment.GeneralMDP import MDP
from EthicsPlanner.Environment.Theory.Absolutism import Absolutism

class Absolute(Absolutism):
    

    def JudgeTransition(self, successor:MDP.Successor):
        return successor.targetState.props['forbidden']

    def StateHeuristic(self, state:MDP.State):
        return False
