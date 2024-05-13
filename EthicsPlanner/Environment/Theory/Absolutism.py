from EthicsPlanner.Environment.GeneralMDP import MDP
from EthicsPlanner.Environment.Result import AttackResult
from EthicsPlanner.Environment.Theory.MoralTheory import MoralTheory
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
        if e1==False and e2==True:
            return AttackResult.ATTACK
        if e1==True and e2==False:
            return AttackResult.REVERSE
        return AttackResult.DRAW
    
    def EmptyEstimate(self):
        return False

    def IsConverged(self, V, V_, epsilon=0.0001):
        return V==V_

    def StateHeuristic(self, state:MDP.State):
        return False
    
    def EstimateString(self, estimate):
        if estimate:
            return 't'
        return 'f'

    def GatherString(self, successors, E):
        out = []
        for s in successors:
            out.append("{j} OR {k}".format(j=self.JudgeTransition(s), k=E[s.targetState.id]))
        return out

