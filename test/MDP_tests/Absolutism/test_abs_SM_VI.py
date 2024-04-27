from Raspberry.Environment.Abstract.AbstractProblem import AbstractProblem
from Raspberry.Planner.MDP_Solvers.SM_ValueIteration import Singleton_ValueIteration
import Raspberry.Environment.Abstract.AbstractGenerator as ag
from Raspberry.Environment.Abstract.Absolute import Absolute
import test.checkPolicy as checkPolicy


def test_crashTest():
    d = ag.setupFunctionFromFile('test/SavedAbstractEnvs/noChoice.json')
    ssp = AbstractProblem(setup=d,theories=[[Absolute()]])
    solver = Singleton_ValueIteration(theoryTag='absolute')
    pi = solver.solve(ssp)


def test_ProbabilisticDoubleAction():
    d = ag.setupFunctionFromFile('test/SavedAbstractEnvs/probDoubleAction.json')
    mdp = AbstractProblem(setup=d,theories=[[Absolute()]])
    solver = Singleton_ValueIteration(theoryTag='absolute')
    pi = solver.solve(mdp)
    assert pi[0]=='B'


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
    mdp = AbstractProblem(setup=new,theories=[[Absolute()]])
    pi = Singleton_ValueIteration(theoryTag='absolute').solve(mdp)
    #mdp.VisualiseCompleteGraph('tempCompGraph')
    checkPolicy.check(mdp, solStateTiles, solActions, pi)