from Raspberry.Environment.GeneralMDP import MDP
from Raspberry.Environment.Result import AttackResult
from Raspberry.Environment.Theory.MoralTheory import MoralTheory
import numpy as np

class Tile(MoralTheory):
    def __init__(self) -> None:
        self.tag='tile'

    def JudgeState(self, state:MDP.State):
        return state.props['tile']

    def JudgeTransition(self, successor:MDP.Successor):
        return str(successor.sourceState.props['tile']) + "->" + str(successor.targetState.props['tile'])
    
    def Gather(self, successors, E, probabilities=None):
        return successors[0].sourceState.props['tile']


    def LEQJudgement(self, j1, j2)->AttackResult:
        return AttackResult.DRAW

    # Use estimates in value function to build expected utility of judgement + successors
    def EstimateUnion(self, V, judgement, successors, ssp):
        return judgement

    def EmptyEstimate(self):
        return -1

    def CompareEstimates(self, e1,e2)->AttackResult:
        return AttackResult.DRAW

    def IsConverged(self, V, V_, epsilon):
        return True

    def StateHeuristic(self, state:MDP.State):
        return state.props['tile']