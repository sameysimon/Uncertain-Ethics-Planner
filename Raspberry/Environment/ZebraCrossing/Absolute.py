from Raspberry.Environment.GeneralMDP import MDP
from Raspberry.Environment.Theory.Absolutism import Absolutism

class Absolute(Absolutism):


    def JudgeTransition(self, successor:MDP.Successor):
        if successor.sourceState.props['elders-harmed'] > successor.targetState.props['elders-harmed']:
            return True