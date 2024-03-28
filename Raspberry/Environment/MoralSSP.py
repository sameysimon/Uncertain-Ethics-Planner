from Raspberry.Environment.MultiMoralMDP import MM_MDP
from Raspberry.Environment.SingletonMoralMDP import SM_MDP
from Raspberry.Environment.GeneralMDP import MDP
from abc import ABC, abstractmethod 
import numpy as np

class MSSP(MDP,ABC):
    def __init__(self, discount=0.9):
        super().__init__()
        self.discount=discount

    @abstractmethod
    def Reward(self, state: MDP.State, action: str) -> float:
        pass

    @abstractmethod
    def isGoal(self, state: MDP.State):
        pass

    @abstractmethod
    def getStateHeuristic(self, state: MDP.State) -> dict:
        pass


class MM_SSP(MM_MDP, MSSP, ABC):
    def __init__(self, discount=0.9):
        super().__init__()
        self.discount=discount

    def setValuation(self, V, state, action):
        super().setValuation(V, state, action)
        successors = self.getActionSuccessors(state, action)
        V['reward'][state.id] = self.Reward(state, action) + sum([s.probability*V['reward'][s.targetState.id]*self.discount for s in successors])

    def isConverged(self, V, V_, epsilon=0.001):
        if super().isConverged(V, V_, epsilon):
            # If morals have converged, then True if reward converged too.
            v = np.array(V['reward'])
            v_ = np.array(V_['reward'])
            return np.linalg.norm(v_ - v, np.inf) < epsilon
        # Morals have not converged.
        return False


class SM_SSP(SM_MDP, MSSP, ABC):
    def __init__(self, discount=0.9):
        super().__init__()
        self.discount=discount