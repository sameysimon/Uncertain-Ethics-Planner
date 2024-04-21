from Raspberry.Environment.GeneralMDP import MDP
from Raspberry.Environment.Theory.Absolutism import Absolutism

class NoLies(Absolutism):

    def JudgeTransition(self, successor:MDP.Successor):
        # if action is to lie compare, judge transition bad.
        return False