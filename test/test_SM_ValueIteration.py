from Raspberry.Environment.Abstract.AbstractProblems import AbstractWorld_SM_MDP
from Raspberry.Planner.SM_ValueIteration import Solver

def test_crashTest():
    d={}
    d['cost']=-1
    d['goalTiles']=[]
    d['actions'] = {0:['A'], 1:['A'], 2:['A'], 3:['A']}
    d['utilities'] = [0,1,2,3,4]

    # Initialise state space successor dicts
    d['stateSpace'] = [{},{},{},{}]
    
    # List of successor (tile,probability) for each state-action
    d['stateSpace'][0]['A'] = [(1,1)]

    d['stateSpace'][1]['A'] = [(2,1)]
    
    d['stateSpace'][2]['A'] = [(3,1)]

    d['stateSpace'][3]['A'] = []

    ssp = AbstractWorld_SM_MDP(setup=d)
    solver = Solver()
    pi = solver.solve(ssp)


def test_ProbabilisticDoubleAction():
    # Only two competing actions on the first state.
    # Each successor of state 1 has two successors each.
    # A's successor has -1 expected utility; B's successor has 1 expected utility. 
    # To apply/back-prop the utility, must take action in successors of A/B.
    # Best policy takes action B in state 0.
    d={}
    d['cost']=-1
    d['goalTiles']=[]
    d['actions'] = {0:['A','B'], 1:['A'], 2:['A'], 3:['A'], 4:['A'], 5:[],6:[],7:[],8:[],9:[]}
    d['utilities'] = [0, -3,1, -1,3, 0,0,0,0,0]

    # Initialise state space successor dicts
    d['stateSpace'] = [{} for i in range(0,9)]
    
    # List of successor (tile,probability) for each state-action
    d['stateSpace'][0]['A'] = [(1,0.5), (2,0.5)]

    d['stateSpace'][0]['B'] = [(3,0.5), (4,0.5)]

    d['stateSpace'][1]['A'] = [(5,1)]
    d['stateSpace'][2]['A'] = [(6,1)]
    d['stateSpace'][3]['A'] = [(7,1)]
    d['stateSpace'][4]['A'] = [(8,1)]

    ssp = AbstractWorld_SM_MDP(setup=d)
    solver = Solver()
    pi = solver.solve(ssp)
   

    assert pi[0]=='B'