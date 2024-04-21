from abc import ABC, abstractmethod 
from copy import deepcopy

class MDP(ABC):
    class State:
        def __init__(self, _index=0, _props={}):
            self.id = _index
            self.actions = []
            self.props = _props
            self.successors = {}
            self.ancestors = []
            
    class Successor:
        def __init__(self, _sourceState, _targetState, _probability, _action):
            self.sourceState = _sourceState
            self.targetState = _targetState
            self.probability = _probability
            self.action = _action

    def __init__(self):
        self.states = [] # List of explicit instantiated states
        self.rules = [] # List of rule functions for state-action transitions
        self.__statePropIndex = {}
        self.__expandedStates = [] # State indices of fully expanded states (has State, successors)
        self.infinite = False
        
    def makeAllStatesExplicit(self):
        if self.infinite:
            return False
        idx = 0
        while idx < len(self.states):
            actions = self.getActions(self.states[idx])
            for a in actions:
                self.getActionSuccessors(self.states[idx], a)
            idx+=1
        return True
    
    # If a rule has 5 outcomes, one of the  can be changed, and four more must 
    def getActionSuccessors(self, state: State, action:str, readOnly=False):
        if action in state.successors.keys():
            return state.successors[action]
        if readOnly:
            return []
        # Create successors since they are not in the dict.
        s = self.__buildSuccessors(state, action)
        return s

    def __buildSuccessors(self, state: State, action:str):
        successorsValues = [(state.props, 1)]
        for ruleFunc in self.rules:
            ruleSuccessorsValues = []
            for existing in successorsValues:
                ruleSuccessorsValues.extend(ruleFunc(self, existing[0], existing[1], action))
            successorsValues = ruleSuccessorsValues
        
        state.successors[action] = []
        for targetProperties, probability in successorsValues:
            successorState = MDP.Successor(state, self.stateFactory(targetProperties), probability, action)
            state.successors[action].append(successorState)
        return state.successors[action]

    # I don't remember what this does :(
    def getPropStr(stateProps):
        pass

    def stateFactory(self, stateProps):
        propStr = str(stateProps)
        if propStr in self.__statePropIndex.keys():
            return self.states[self.__statePropIndex[propStr]]

        index = len(self.states)
        self.__statePropIndex[propStr] = index
        self.states.append(MDP.State(_index=index, _props = stateProps))
        return self.states[self.__statePropIndex[propStr]]

    def expandState(self, state:State):
        # MAKE SURE THIS WORKS
        self.__expandedStates.append(state.id)
        oldStateCount = len(self.states)
        actions = self.getActions(state)
        for actionStr in actions:
            successors = self.getActionSuccessors(state, actionStr)
            for successor in successors:
                [self.getActionSuccessors(successor.targetState, a) for a in self.getActions(successor.targetState)]
        
        newStates = []
        for i in range(oldStateCount, len(self.states)):
            newStates.append(self.states[i])
        return newStates

    def printPolicy(ssp, pi):
        return

    def getPaths(self, pi, currentState=None, currentPath=[]):
        if currentState.id in pi.keys():
            successors = self.getActionSuccessors(currentState, pi[currentState.id])
            if len(successors)==0:
                yield currentPath
            for childSuccessor in successors:
                if not (childSuccessor.targetState.id in currentPath):
                    cpy = deepcopy(currentPath)
                    cpy.append(childSuccessor)
                    yield from self.getPaths(pi, childSuccessor.targetState, cpy)
                else:
                    yield currentPath
        else:        
            yield currentPath
