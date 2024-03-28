from Raspberry.Environment.MoralSSP import MDP
from Raspberry.Environment.Result import AttackResult
from Raspberry.Environment.Theory.MoralTheory import MoralTheory
import numpy as np

class Absolutism(MoralTheory):
    
    def __init__(self, _ssp) -> None:
        super().__init__(_ssp)
        self.badActions = []
        self.badStates = []
        self.tag='absolute'
    
    def JudgeTransition(self, successor):
        if successor.action in self.badActions:
            return True # Violations
        if successor.targetState in self.badStates:
            return True # Violations
        return False
    
    def Gather(self, successors, E):
        j = False # Assume no violations
        for s in successors:
            if self.JudgeTransition(s):
                return True
            if E[s.targetState.id]:
                return True
        return False


    def LEQJudgement(j1, j2)->bool:
        pass

    def EstimateUnion(judgement, alternatives):
        pass

    def CompareEstimates(e1,e2)->bool:
        pass
    
    def EmptyEstimate():
        pass