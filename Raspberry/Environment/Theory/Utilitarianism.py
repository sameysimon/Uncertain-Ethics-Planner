from Raspberry.Environment.MoralSSP import MDP
from Raspberry.Environment.Result import AttackResult
from Raspberry.Environment.Theory.MoralTheory import MoralTheory
import numpy as np

class Utilitarianism(MoralTheory):
    def __init__(self, discount=0.9) -> None:
        self.tag='utility'
        self.discount=discount

    def JudgeState(self, state:MDP.State):
        return state.props['utility']

    def JudgeTransition(self, successor:MDP.Successor):
        return successor.targetState.props['utility']
    
    def IntegrateJudgments(self, j1, j2):
        return j1 + j2
    
    def LEQJudgement(self, j1, j2)->AttackResult:
        if j1 > j2:
            return AttackResult.ATTACK
        if j1 < j2:
            return AttackResult.REVERSE
        return AttackResult.DRAW

    # Use estimates in value function to build expected utility of judgement + successors
    # In effect, passes in (Judgement, [(estimate, probability)])
    # This is used as to E = R(s) + Sum_s'[P(s,a,s') * E(s') * discount]
    def EstimateUnion(self, judgement, estimates, probabilities, ssp):
        union = judgement
        for i in range(len(estimates)):
            union += self.discount * probabilities[i] * estimates[i]
        return union

    # Given state-action-state transition, adds judgement to estimates for back-propagation
    # In effect, parameters are: ([(judgement, probability)], [Estimates])
    #  = Sum_s' [ P(s,a,s')*[R(s,a,s') + E(s')] ]
    def Gather(self, judgments, probabilities, estimates):
        g = 0
        for i in range(len(estimates)):
            g +=  probabilities[i] * (judgments[i] + (self.discount * estimates[i]))
        return g

    
    
    def EmptyEstimate(self):
        return 0

    def CompareEstimates(self, e1,e2)->AttackResult:
        if e1 > e2:
            return AttackResult.ATTACK
        if e1 < e2:
            return AttackResult.REVERSE
        return AttackResult.DRAW

    def IsConverged(self, V, V_, epsilon=0.0001):
        v = np.array([s['utility'] for s in V])
        v_ = np.array([s['utility'] for s in V_])
        
        return np.linalg.norm(v_ - v, np.inf) < epsilon

    def StateHeuristic(self, state:MDP.State):
        return 0        
        






