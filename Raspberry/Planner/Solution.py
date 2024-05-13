import copy

class BestSubGraph:
    def __init__(self, startStateIndex, mdp, record=True):
        self.V={}
        self.appendToV(mdp.getStateHeuristic(mdp.states[startStateIndex]))

        self.pi = {}
        self.states = [startStateIndex]
        self.stateSuccessors = {}
        self.expandedStates = []


    def appendToV(self, theoryValues:dict):
        for tag, value in theoryValues.items():
            self.V.setdefault(tag,[]).append(value)

    def getUnexpandedStatesInBPSG(self, Gmdp):
        x = []
        for s in self.states:
            if s in self.expandedStates:
                continue
            x.append(s)
        return x

  

    def update(self, Gmdp):
        startState = self.states[0]
        self.states = [] # Clear all except the start state
        self.stateSuccessors = {}
        self.__addBestStates(Gmdp, startState)

    def __addBestStates(self, Gmdp, stateInd):
        state = Gmdp.states[stateInd]
        self.states.append(stateInd)
        if not stateInd in self.pi.keys():
            return

        stateBestAction = self.pi[stateInd]
        
        for s in state.successors[stateBestAction]:
            self.stateSuccessors.setdefault(stateInd, [])
            if s.targetState.id in self.stateSuccessors[stateInd]:
                continue
            self.stateSuccessors[stateInd].append(s.targetState.id)
            if s.targetState.id in self.states:
                continue
            self.__addBestStates(Gmdp, s.targetState.id)

    def updateValuation(self, Gmdp, newStates):
        if newStates==None:
            return
        numOfStatesInV = len(self.V[list(self.V.keys())[0]])
        for i in range(numOfStatesInV, numOfStatesInV + len(newStates)):
            self.appendToV(Gmdp.getStateHeuristic(Gmdp.states[i]))
