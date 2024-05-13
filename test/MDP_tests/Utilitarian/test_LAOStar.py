from Raspberry.Planner.MDP_Solvers.iLAOStar import HeuristicSolver
from Raspberry.Environment.Abstract.AbstractProblem import AbstractProblem
import Raspberry.Environment.Abstract.AbstractGenerator as ag



def test_ProbabilisticDoubleAction():
    # Only two competing actions on the first state.
    # Each successor of state 1 has two successors each.
    # A's successor has -1 expected utility; B's successor has 1 expected utility. 
    # To apply/back-prop the utility, must take action in successors of A/B.
    # Best policy takes action B in state 0.
    d = ag.setupFunctionFromFile('test/SavedAbstractEnvs/probDoubleAction.json')

    mdp = AbstractProblem(setup=d)
    solver = HeuristicSolver()
    bpsg = solver.solve(mdp)
    #mdp.VisualiseCompleteGraph('test/graphs/completeProbDouble')
    #mdp.VisualiseExplicitGraph(solution=bpsg, fileName='test/graphs/policyProbDouble')

    assert bpsg.pi[0]=='B'

def test_env_1():
    from_file(fileName='test/SavedAbstractEnvs/testEnv1.json',
    solStateTiles=[0,1,2,3,11,57,81,82],
    solActions=['0','1','0','0','0','0','0','0'])
    


def from_file(fileName, solStateTiles, solActions):
    new = ag.setupFunctionFromFile(fileName=fileName)
    mdp = AbstractProblem(setup=new)
    solver=HeuristicSolver()
    bpsg = solver.solve(mdp)
    #mdp.VisualiseCompleteGraph('tempCompGraph.pdf')
    #mdp.VisualiseExplicitGraph(bpsg, 'tempExpGraph.pdf')
    solStates = {}
    for s in mdp.states:
        if s.props['tile'] in solStateTiles:
            solStates[solStateTiles.index(s.props['tile'])] = s

    assert len(solStates) == len(solStateTiles)

    for idx, s in solStates.items():
        assert bpsg.pi[s.id] == str(solActions[idx])