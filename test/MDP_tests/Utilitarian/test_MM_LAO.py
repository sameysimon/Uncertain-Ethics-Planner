from EthicsPlanner.Environment.Abstract.AbstractProblem import AbstractProblem
from EthicsPlanner.Planner.MDP_Solvers.MM_Heuristic import Solver
import EthicsPlanner.Environment.Abstract.AbstractGenerator as ag
import test.checkPolicy as checkPolicy


def test_crashTest():
    d = ag.setupFunctionFromFile('test/SavedAbstractEnvs/noChoice.json')
    mdp = AbstractProblem(setup=d)
    solver = Solver()
    pi = solver.solve(mdp)


def test_ProbabilisticDoubleAction():
    d = ag.setupFunctionFromFile('test/SavedAbstractEnvs/probDoubleAction.json')
    mdp = AbstractProblem(setup=d)
    solver = Solver()
    bpsg = solver.solve(mdp)
    assert bpsg.pi[0]=='B'


def test_env_1():
    from_file(fileName='test/SavedAbstractEnvs/testEnv1.json',
    solStateTiles=[0,1,2,3,11,57,81,82],
    solActions=['0','1','0','0','0','0','0','0'])



def from_file(fileName, solStateTiles, solActions):
    new = ag.setupFunctionFromFile(fileName=fileName)
    mdp = AbstractProblem(setup=new)
    bpsg = Solver().solve(mdp)
    #mdp.VisualiseCompleteGraph('tempCompGraph')
    #mdp.VisualiseExplicitGraph(bpsg, 'tempExpGraph')
    checkPolicy.check(mdp, solStateTiles, solActions, bpsg.pi)