from Raspberry.Environment.Abstract.AbstractSMMDP import AbstractWorld
import numpy as np
import json
import copy

# Generates abstract problems with properties

defaultValues = {
    'stateSpace':{},
    'utilities':[],
    'cost' : -1,
    'actions':{},
    'goalTiles':[1]
}

def getRandomProbability(rng, remainingItems, remainingProbability,digits=2):
    if remainingItems==1:
        p = round(remainingProbability, digits)
        if p<0:
            print()
        return p
    evenChance = (remainingProbability)/(remainingItems)
    p = rng.normal(loc=evenChance,scale=0.25)
    p = round(p,digits)
    if p<0:
        p=0.05
    if p>1:
        p=0.95
    return p



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
            allSuccessorsProb = 0
            for s in range(noSuccessors):
                # Successor goes at end of state space.
                successorState = len(_stateSpace)

                p = getRandomProbability(rng, noSuccessors-s, 1-allSuccessorsProb)
                allSuccessorsProb+=p
                # Add successor to state space
                _stateSpace[_state][a].append((successorState, p))
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
        u.append(rng.integers(-10,11))

    potentialGoals = leaves
    if goalsAsLeaves==False:
        potentialGoals=range(len(ss))
    else:
        potentialGoals = leaves

    for i in range(len(goals)+1):
        c = rng.choice(potentialGoals)
        goals.append(c)
        potentialGoals.remove(c)

    return {'utilities':u, 'stateSpace':ss, 'cost':-1, 'actions':acts, 'goalTiles':goals}
        


def setupFunctionFromFile(fileName):
    file = open(fileName+'.json','r')
    t = file.read()
    params = json.loads(t)
    def setup():
        AbstractWorld.cost=params['cost']
        AbstractWorld.goalTiles=params['goalTiles']
        AbstractWorld.actions = params['actions']
        AbstractWorld.utilities = params['utilities']
        AbstractWorld.stateSpace = params['stateSpace']

    return setup

def saveSetupParams(fileName, params):
    with open(fileName+'.json', 'w') as f:
        json.dump(params, f)
    
