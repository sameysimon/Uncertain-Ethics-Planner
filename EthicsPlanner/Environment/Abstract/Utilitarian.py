from EthicsPlanner.Environment.GeneralMDP import MDP
from EthicsPlanner.Environment.Theory.Utilitarianism import Utilitarianism

class Utilitarian(Utilitarianism):

    def JudgeState(self, state:MDP.State):
        return state.props['utility']

    def JudgeTransition(self, successor:MDP.Successor):
        return successor.targetState.props['utility']
    
    def StateHeuristic(self, state:MDP.State):
        return 20