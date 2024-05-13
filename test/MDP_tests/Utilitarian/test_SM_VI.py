from EthicsPlanner.Environment.Abstract.AbstractProblem import AbstractProblem
from EthicsPlanner.Planner.MDP_Solvers.SM_ValueIteration import Singleton_ValueIteration
import EthicsPlanner.Environment.Abstract.AbstractGenerator as ag

def test_crashTest():

    d = ag.setupFunctionFromFile('test/SavedAbstractEnvs/noChoice.json')
    mdp = AbstractProblem(setup=d)
    solver = Singleton_ValueIteration()
    pi = solver.solve(mdp)


def test_ProbabilisticDoubleAction():
    d = ag.setupFunctionFromFile('test/SavedAbstractEnvs/probDoubleAction.json')
    mdp = AbstractProblem(setup=d)
    solver = Singleton_ValueIteration()
    pi = solver.solve(mdp)
    assert pi[0]=='B'


def test_env_1():
    from_file(fileName='test/SavedAbstractEnvs/testEnv1.json',
    solStateTiles=[0,1,2,3,11,57,81,82],
    solActions=['0','1','0','0','0','0','0','0'])

def test_env_2():
    from_file(fileName='test/SavedAbstractEnvs/testEnv2.json',
    solStateTiles=[0,4,87,88,89,5,117,6,157],
    solActions=[1,1,0,0,0,1,0,0,0])


def from_file(fileName, solStateTiles, solActions):
    new = ag.setupFunctionFromFile(fileName=fileName)
    mdp = AbstractProblem(setup=new)
    solver=Singleton_ValueIteration()
    pi = solver.solve(mdp)
    #mdp.VisualiseCompleteGraph('tempCompGraph.pdf')
    #mdp.VisualiseExplicitGraph(bpsg, 'tempExpGraph.pdf')
    solStates = {}
    for s in mdp.states:
        if s.props['tile'] in solStateTiles:
            solStates[solStateTiles.index(s.props['tile'])] = s

    assert len(solStates) == len(solStateTiles)

    for idx, s in solStates.items():
        assert pi[s.id] == str(solActions[idx])