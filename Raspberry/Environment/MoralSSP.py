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

class SM_SSP(SM_MDP, MSSP, ABC):
    def __init__(self, discount=0.9):
        super().__init__()
        self.discount=discount