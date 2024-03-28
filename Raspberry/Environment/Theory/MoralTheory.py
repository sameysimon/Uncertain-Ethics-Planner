from abc import abstractmethod, ABC

class MoralTheory(ABC):
    def __init__(self, _ssp) -> None:
        self.ssp = _ssp


    @abstractmethod
    def EmptyEstimate():
        pass

    @abstractmethod
    def JudgeState(self, state):
        pass

    @abstractmethod
    def JudgeTransition(self, successor):
        # Return judgement from successor (sourceState,action,targetState)
        pass
    
    def Gather(self, successors:list, E:list, probabilities:list=None):
        # Return estimate by coalesced successor judgments, plus estimate function
        pass

    @abstractmethod
    def LEQJudgement(j1, j2)->bool:
        pass

    @abstractmethod
    def CompareEstimates(e1,e2)->bool:
        pass

    @abstractmethod
    def EstimateUnion(judgement, alternatives):
        pass


    