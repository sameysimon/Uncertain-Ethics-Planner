from abc import abstractmethod, ABC

class MoralTheory(ABC):
    def __init__(self, _ssp) -> None:
        self.ssp = _ssp

    @abstractmethod
    def JudgeState(state):
        pass

    """ @abstractmethod
    def JudgeTransition(successor):
        pass """
    
    @abstractmethod
    def LEQJudgement(j1, j2)->bool:
        pass

    @abstractmethod
    def EstimateUnion(judgement, alternatives):
        pass

    @abstractmethod
    def CompareEstimates(e1,e2)->bool:
        pass
    
    @abstractmethod
    def EmptyEstimate():
        pass
    
    def Gather(self, state, action, solution=None) -> any:
        # Evaluates a state-action by its successors, given a value function.
        pass

    def Estimate(self, state, policy):
        # Evaluates a policy at a state.
        pass