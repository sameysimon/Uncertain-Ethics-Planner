from EthicsPlanner.Environment.GeneralMDP import MDP
from EthicsPlanner.Environment.Theory.Absolutism import Absolutism

class NoLies(Absolutism):

    def JudgeTransition(self, successor:MDP.Successor):
        # if action is to lie compare, judge transition bad.
        if successor.action=='neg_lie' or successor.action=='pos_lie':
            return True
        return False

    def StateHeuristic(self, state:MDP.State):
        return False
