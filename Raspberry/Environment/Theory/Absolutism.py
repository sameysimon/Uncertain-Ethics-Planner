from Raspberry.Environment.MoralSSP import MDP
from Raspberry.Environment.Result import AttackResult
from Raspberry.Environment.Theory.MoralTheory import MoralTheory
import numpy as np

class Absolutism(MoralTheory):
    
    def __init__(self) -> None:
        self.tag='absolute'
    
    def Gather(self, successors, E, probabilities=None):
        for s in successors:
            if self.JudgeTransition(s):
                return True
            if E[s.targetState.id]:
                return True
        return False

    def CompareEstimates(self, e1,e2)->AttackResult:
        if not e1 and e2:
            return AttackResult.ATTACK
        if e2 and not e1:
            return AttackResult.REVERSE
        return AttackResult.DRAW
    
    def EmptyEstimate(self):
        return False

    def IsConverged(self, V, V_, epsilon=0.0001):
        return V==V_

    def StateHeuristic(self, state:MDP.State):
        return False