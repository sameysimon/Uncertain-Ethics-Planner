from Raspberry.Environment.Abstract.AbstractProblem import AbstractProblem
import Raspberry.Environment.Abstract.AbstractGenerator as ag

def test_defaultTree():
    setup = ag.randomTreeSetup(maxBranchFactor=3, maxActionFactor=2)
    ssp = AbstractProblem(setup=setup)
    ssp.VisualiseCompleteGraph(fileName='test/abstractGeneratorTest')
    for state in ssp.world['stateSpace']:
        for action in state:
            p = 0
            for successor in state[action]:
                p+= successor[1]
            assert p==1