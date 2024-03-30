from Raspberry.Environment.Abstract.AbstractProblems import AbstractWorld_MM_SSP
from Raspberry.Planner.MM_FindRevise import Solver
import Raspberry.Environment.Abstract.AbstractGenerator as ag

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

    ssp = AbstractWorld_MM_SSP(setup=d)
    solver = Solver()
    bpsg = solver.solve(ssp)

def test_DoubleAction():
    # Only two competing actions on the first state.
    # A's successor has -1 utility; B's successor has 1 utility. 
    # To apply/back-prop the utility, must take action in A/B.
    # Best policy takes action B in state 0.

    d={}    
    d['cost']=-1
    d['goalTiles']=[]
    d['actions'] = {0:['A','B'], 1:['A'], 2:['A'], 3:[], 4:[]}
    d['utilities'] = [0,-1,1,0,0]

    # Initialise state space successor dicts
    d['stateSpace'] = [{} for i in range(0,5)]
    
    # List of successor (tile,probability) for each state-action
    d['stateSpace'][0]['A'] = [(1,1)]
    d['stateSpace'][0]['B'] = [(2,1)]

    d['stateSpace'][1]['A'] = [(3,1)]
    d['stateSpace'][2]['A'] = [(4,1)]


    ssp = AbstractWorld_MM_SSP(setup=d)
    solver = Solver()
    bpsg = solver.solve(ssp)
    ssp.VisualiseCompleteGraph('test/completeDouble')
    ssp.VisualiseExplicitGraph(solution=bpsg, fileName='test/policyDouble')

    # Explored an alternative+two states on final solution.
    assert len(bpsg.pi)>=2
    # Final policy decision is correct.
    assert bpsg.pi[0]=='B'    


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


    ssp = AbstractWorld_MM_SSP(setup=d)
    solver = Solver()
    bpsg = solver.solve(ssp)
    ssp.VisualiseCompleteGraph('test/completeProbDouble')
    ssp.VisualiseExplicitGraph(solution=bpsg, fileName='test/policyProbDouble')

    assert bpsg.pi[0]=='B'

def test_random_medium():    
    # 3^(3*3)= 19K max total states 
    # maximum 3 actions per state, 3 branches per action, max depth=3
    # Trial 1
    setup = ag.randomTreeSetup(maxBranchFactor=3, maxActionFactor=3, depth=3, seed=10101)
    ssp = AbstractWorld_MM_SSP(setup=setup)
    solver = Solver()
    bpsg = solver.solve(ssp)

    # Trial 2
    setup = ag.randomTreeSetup(maxBranchFactor=3, maxActionFactor=3, depth=3, seed=20202)
    ssp = AbstractWorld_MM_SSP(setup=setup)
    solver = Solver()
    bpsg = solver.solve(ssp)

    # Trial 3
    setup = ag.randomTreeSetup(maxBranchFactor=3, maxActionFactor=3, depth=3, seed=854543)
    ssp = AbstractWorld_MM_SSP(setup=setup)
    solver = Solver()
    bpsg = solver.solve(ssp)

def test_random_wide():
    # maximum 3 actions per state, 5 branches per action, max depth=3
    # 3^(5*3)= 14M max total states
    setup = ag.randomTreeSetup(maxBranchFactor=5, maxActionFactor=3, depth=3, seed=10101)
    ssp = AbstractWorld_MM_SSP(setup=setup)
    solver = Solver()
    bpsg = solver.solve(ssp)

def test_random_long():
    # maximum 3 actions per state, 3 branches per action, max depth=5
    # 5^(3*3)= 1.9M max total states
    setup = ag.randomTreeSetup(maxBranchFactor=3, maxActionFactor=3, depth=5, seed=10101)
    ssp = AbstractWorld_MM_SSP(setup=setup)
    solver = Solver()
    bpsg = solver.solve(ssp)
    print()



def old(ssp,bpsg):
    tileOneInd=0
    tileTwoInd=0
    tileThreeInd = 0
    tileFourInd = 0
    for ind, s in enumerate(ssp.states):
        if s.props['tile']==1:
            tileOneInd = ind
        if s.props['tile']==2:
            tileTwoInd = ind
        if s.props['tile']==3:
            tileThreeInd = ind
        if s.props['tile']==4:
            tileFourInd = ind

    # Defo a be better way of doing this.
    assert tileTwoInd!=tileOneInd
    assert tileThreeInd!= tileFourInd

    # Expected: Go to state +ve utility state 3 with aB
    assert bpsg.pi[tileOneInd]=='B'
    # Tile 2 should go to goal state, instead of looping on bad state.
    assert bpsg.pi[tileTwoInd]=='B'
    # Tile 3 should go to to goal state, instead of looping on itself
    assert bpsg.pi[tileThreeInd]=='A'
    