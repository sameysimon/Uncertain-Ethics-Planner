from EthicsPlanner.Environment.MultiMoralMDP import MM_MDP
from EthicsPlanner.Environment.Result import AttackResult
from EthicsPlanner.Environment.Theory.MoralTheory import MoralTheory
import numpy as np

class Utilitarianism(MoralTheory):
    def __init__(self, discount=0.9) -> None:
        self.tag='utility'
        self. discount=discount



    def EmptyEstimate(self):
        return 0

    def CompareEstimates(self, e1,e2)->AttackResult:
        if e1 > e2:
            return AttackResult.ATTACK
        if e1 < e2:
            return AttackResult.REVERSE
        return AttackResult.DRAW

    def IsConverged(self, V, V_, epsilon=0.0001):
        v = np.array(V)
        v_ = np.array(V_) 
        return np.linalg.norm(v_ - v, np.inf) < epsilon

    def StateHeuristic(self, state:MM_MDP.State):
        return 0        


    # Given state-action-state transition, adds judgement to estimates for back-propagation
    # In effect, parameters are: ([(judgement, probability)], [Estimates])
    #  = Sum_s' [ P(s,a,s')*[R(s,a,s') + E(s')] ]
    def Gather(self, successors, E, probabilities=None):
        g = 0
        if probabilities==None:
            probabilities=[]
            for s in successors:
                probabilities.append(s.probability)
        
        for idx, s in enumerate(successors):
            eu =  probabilities[idx] * (self.JudgeTransition(s) + (E[s.targetState.id]*self.discount))
            g += eu
        return g


    def EstimateString(self, estimate):
        return str(round(estimate, 3))

    def GatherString(self, successors, E):
        out = []
        for s in successors:
            out.append("{p}* ({j}+{g}*{k})".format(p=s.probability, j=self.JudgeTransition(s), g=self.discount, k=self.EstimateString(E[s.targetState.id])))
        return out