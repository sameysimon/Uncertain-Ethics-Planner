from abc import abstractmethod, ABC

class MoralTheory(ABC):

    @abstractmethod
    def EmptyEstimate():
        pass

    @abstractmethod
    def JudgeTransition(self, successor):
        # Return judgement from successor (sourceState,action,targetState)
        pass
    
    def Gather(self, successors:list, E:list, probabilities:list=None):
        # Return estimate by coalesced successor judgments, plus estimate function
        pass

    @abstractmethod
    def CompareEstimates(e1,e2)->bool:
        pass


    @abstractmethod
    def IsConverged(self, V, V_, epsilon=0.0001):
        pass

    def StateHeuristic(self, state):
        return False

    