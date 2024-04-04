from Raspberry.Environment.SingletonMoralMDP import SM_MDP
from Raspberry.Environment.MoralSSP import MM_SSP
from Raspberry.Environment.Abstract.Utilitarian import Utilitarian
from Raspberry.Environment.Abstract.Tile import Tile
from Raspberry.Environment.Abstract.Abstract import AbstractBase


#
# Markov Decision Problems:
#


#
# Singleton Moral Theory MDP problem (one theory, no rewards, no goals)
#
class AbstractWorld_SM_MDP(SM_MDP, AbstractBase):
    def __init__(self, setup=None):
        SM_MDP.__init__(self)
        AbstractBase.__init__(self, setup)
        self.Theory = Utilitarian() # Set the ethical theories
        
    # ****
    # Action
    # ****
    def getActions(self, state:SM_MDP.State) -> list:
        return self.world['actions'][state.props['tile']]



"""
class AbstractWorld_MM_MDP(MM_MDP, AbstractBase):
    def __init__(self, setup=None):
        SM_MDP.__init__(self)
        AbstractBase.__init__(self, setup)
        self.TheoryClasses = [[Utilitarian()]] # Set the ethical theories
        
    # ****
    # Action
    # ****
    def getActions(self, state:SM_MDP.State) -> list:
        return self.world['actions'][state.props['tile']]
"""


#
# Stochastic Shortest Path Problems:
#

"""
class AbstractWorld_SM_SSP(SM_SSP, AbstractBase):
    def __init__(self, setup=None):
        MM_SSP.__init__(self)
        AbstractBase.__init__(self, setup)
        self.Theory = Utilitarian() # Set the ethical theory
        self.discount = 0.9


    # ****
    # Action, Reward, Heuristic
    # ****
    def getActions(self, state:MM_SSP.State) -> list:
        return self.world['actions'][state.props['tile']]

    def Reward(self, state: MM_SSP.State, action: str) -> float:
        return self.world['cost']

    def isGoal(self, state: MM_SSP.State):
        return state.props['tile'] in self.world['goalTiles']

    def getStateHeuristic(self, state: MM_SSP.State) -> dict:
        h = super().getStateHeuristic(state)
        h['reward'] = abs(4 - state.props['tile'])*-1
        return h
"""


#
# Multi-Moral Theory Stochastic Shortest Path Problem (goals, reward, theory list)
#

class AbstractWorld_MM_SSP(MM_SSP, AbstractBase):
    def __init__(self, setup=None):
        MM_SSP.__init__(self)
        AbstractBase.__init__(self, setup)
        self.TheoryClasses = [[Utilitarian(), Tile()]] # Set the ethical theories
        self.discount = 0.9


    # ****
    # Action, Reward, Heuristic
    # ****
    def getActions(self, state:MM_SSP.State) -> list:
        return self.world['actions'][state.props['tile']]

    def Reward(self, state: MM_SSP.State, action: str) -> float:
        return self.world['cost']

    def isGoal(self, state: MM_SSP.State):
        return state.props['tile'] in self.world['goalTiles']

    def getStateHeuristic(self, state: MM_SSP.State) -> dict:
        h = super().getStateHeuristic(state)
        h['reward'] = abs(4 - state.props['tile'])*-1
        return h


    