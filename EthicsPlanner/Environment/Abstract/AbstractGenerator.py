from EthicsPlanner.Environment.Abstract.AbstractProblem import AbstractProblem
import numpy as np
import json
import copy

# Generates abstract problems with properties

defaultValues = {
    'stateSpace':[],
    'utilities':[],
    'cost' : -1,
    'actions':{},
    'goalTiles':[1]
}


def getRandomProbabilities(total):
    a = np.array([abs(np.random.normal(loc=1/total)) for _ in range(total)])
    a /= a.sum()
    a = np.around(a,2)
    return a

# Create a random setup function, with params fixed. State space has tree structure.
def randomTreeSetup(depth=2, maxActionFactor=2, maxBranchFactor=2, seed=1234, goals=0, goalsAsLeaves=True):
    rng = np.random.default_rng(seed)
    def buildStateSpace(_stateSpace, _actions, _leaves, _state, _depth):
        nonlocal rng
        if _depth==0:
            _actions[_state] = []
            _leaves.append(_state)
            return
                
        # Number of actions
        noActions = rng.integers(0,maxActionFactor,endpoint=True)
        actions = [str(a) for a in range(noActions+1)]
        if len(actions)==0:
            _leaves.append(_state)
        _actions[_state]=actions
        
        oldStateCount = len(_stateSpace)
        for a in actions:
            _stateSpace[_state][a] = []
            noSuccessors = rng.integers(1,maxBranchFactor,endpoint=True)
            probabilities = getRandomProbabilities(noSuccessors)
            for s in range(noSuccessors):
                # Successor goes at end of state space.
                successorState = len(_stateSpace)

                # Add successor to state space
                _stateSpace[_state][a].append((successorState, probabilities[s]))
                _stateSpace.append({})
        # Build all the successor states, one level down:
        for s in range(oldStateCount, len(_stateSpace)):
            buildStateSpace(_stateSpace, _actions, _leaves, s, _depth-1)
        
    ss = [{}]
    acts = {}
    u = []
    leaves=[]
    goals=[]
    buildStateSpace(ss,acts,leaves,0,depth)
    for s in ss:
        u.append(float(rng.integers(-10,-1)))

    potentialGoals = leaves
    if goalsAsLeaves==False:
        potentialGoals=range(len(ss))
    else:
        potentialGoals = leaves
    """
    for i in range(len(goals)+1):
        c = rng.choice(potentialGoals)
        goals.append(c)
        potentialGoals.remove(c)
    """
    return {'utilities':u, 'stateSpace':ss, 'cost':-1, 'actions':acts, 'goalTiles':goals}
        


def setupFunctionFromFile(fileName):
    file = open(fileName,'r')
    t = file.read()
    params = json.loads(t)
    return params

def saveSetupParams(fileName, params):
    with open(fileName, 'w') as f:
        json.dump(params, f)
    
