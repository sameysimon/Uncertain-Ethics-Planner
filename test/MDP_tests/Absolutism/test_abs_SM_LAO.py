from Raspberry.Environment.Abstract.AbstractProblem import AbstractProblem
from Raspberry.Planner.MDP_Solvers.SM_Heuristic import Singleton_HeuristicSolver
import Raspberry.Environment.Abstract.AbstractGenerator as ag
import test.checkPolicy as checkPolicy
from Raspberry.Environment.Abstract.Absolute import Absolute


def test_crashTest():
    d = ag.setupFunctionFromFile('test/SavedAbstractEnvs/noChoice.json')
    ssp = AbstractProblem(setup=d, theories=[[Absolute()]])
    solver = Singleton_HeuristicSolver()
    pi = solver.solve(ssp, theoryTag='absolute')


def test_ProbabilisticDoubleAction():
    d = ag.setupFunctionFromFile('test/SavedAbstractEnvs/probDoubleAction.json')
    mdp = AbstractProblem(setup=d, theories=[[Absolute()]])
    solver = Singleton_HeuristicSolver()
    bpsg = solver.solve(mdp, theoryTag='absolute')
    assert bpsg.pi[0]=='B'


def test_env_1():
    from_file(fileName='test/SavedAbstractEnvs/testEnv1.json',
    solStateTiles=[0,4,120,121],
    solActions=['1','0','0','1'])

def test_env_2():
    from_file(fileName='test/SavedAbstractEnvs/testEnv2.json',
    solStateTiles=[0,4,85],
    solActions=['1','0','1'])


def from_file(fileName, solStateTiles, solActions):
    new = ag.setupFunctionFromFile(fileName=fileName)
    mdp = AbstractProblem(setup=new, theories=[[Absolute()]])
    bpsg = Singleton_HeuristicSolver().solve(mdp, theoryTag='absolute')
    #mdp.VisualiseCompleteGraph('tempCompGraph.pdf')
    #mdp.VisualiseExplicitGraph(bpsg, 'tempExpGraph.pdf')
    checkPolicy.check(mdp, solStateTiles, solActions, bpsg.pi)