import copy

class BestSubGraph:
    def __init__(self, startStateIndex, ssp, record=True):
        self.V={}
        self.appendToV(ssp.getStateHeuristic(ssp.states[startStateIndex]))

        self.pi = {}
        self.states = [startStateIndex]
        self.stateSuccessors = {}
        self.expandedStates = []
        self.record = False
        self.ValueHistory = []
        self.PolicyHistory = []


    def appendToV(self, theoryValues:dict):
        for tag, value in theoryValues.items():
            self.V.setdefault(tag,[]).append(value)

    def getUnexpandedStatesInBPSG(self, GSSP):
        x = []
        for s in self.states:
            if s in self.expandedStates:
                continue
            '''if GSSP.isGoal(GSSP.states[s]):
                continue'''
            x.append(s)
        return x

    def DepthFirstSearch(self, onVisitFn):
        def visit(state, colours, fn=None):
            colours[state] = 'v'
            if state in self.stateSuccessors.keys():
                for child in self.stateSuccessors[state]:
                    childColour = colours.setdefault(child, 'u')
                    if childColour == 'u':
                        visit(child, colours, fn)
            if fn:
                fn(state)
        
        colours = {}
        for state in self.states:
            if colours.setdefault(state, 'u')=='u':
                visit(state, colours, onVisitFn)
        return colours

    def update(self, GSSP):
        startState = self.states[0]
        self.states = [] # Clear all except the start state
        self.stateSuccessors = {}
        self.__addBestStates(GSSP, startState)
        if self.record:
            self.ValueHistory.append(copy.deepcopy(self.V))
            self.PolicyHistory.append(copy.deepcopy(self.pi))

    def __addBestStates(self, GSSP, stateInd):
        state = GSSP.states[stateInd]
        self.states.append(stateInd)
        if not stateInd in self.pi.keys():
            return
        '''
        if GSSP.isGoal(state):
            return
        '''     
        stateBestAction = self.pi[stateInd]
        
        for s in state.successors[stateBestAction]:
            self.stateSuccessors.setdefault(stateInd, [])
            if s.targetState.id in self.stateSuccessors[stateInd]:
                continue
            self.stateSuccessors[stateInd].append(s.targetState.id)
            if s.targetState.id in self.states:
                continue
            self.__addBestStates(GSSP, s.targetState.id)

    def updateValuation(self, GSSP, newStates):
        if newStates==None:
            return
        numOfStatesInV = len(self.V[list(self.V.keys())[0]])
        for i in range(numOfStatesInV, numOfStatesInV + len(newStates)):
            self.appendToV(GSSP.getStateHeuristic(GSSP.states[i]))

    def isProper(self, GSSP):
        endStates = filter(lambda s : s not in self.stateSuccessors.keys() or self.stateSuccessors[s]==[], self.states)
        empty = True
        for s in endStates:
            empty = False
            if not GSSP.isGoal(GSSP.states[s]):
                return False
        # If no end states, no goal/terminating states.
        if empty:
            return False

        # Conditions satisfied. Policy is proper.
        return True

    def getHistoryLength(self):
        return len(self.ValueHistory)


