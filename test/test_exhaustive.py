from Raspberry.Environment.Abstract.AbstractProblems import AbstractWorld_MM_SSP
import Raspberry.Environment.Abstract.AbstractGenerator as ag
from Raspberry.Planner.ExhaustiveSolver import Exhaustive

def test_basicSolve():

    # Define state space
    s = [{}] * 4
    
    s[0]['A'] = [(1,0.5), (2,0.5)]
    s[0]['B'] = [(3,1)]

    s[1]['A'] = [(4,1)]
    s[1]['B'] = [(5,1)]

    s[2]['A'] = [(6,1)]
    s[2]['B'] = [(7,1)]

    s[3]['A'] = [(8,1)]
    s[3]['B'] = [(9,1)]

    d = {}
    d['goalTiles']=[4],
    d['actions']= {0:['A','B'], 1:['A', 'B'], 2:['A','B'], 3:['A', 'B'], 4:[],5:[],6:[],7:[],8:[],9:[]},
    d['utilities']= {0:0, 1:0, 2:0, 3:0,4:0,5:0,6:0,7:0,8:0, 9:0},
    d['stateSpace']=s,
    d['cost']=-1
    ssp = AbstractWorld_MM_SSP(setup=d)
    # Make image of tree
    #ssp.VisualiseCompleteGraph('abstractTest')
    #solver = Exhaustive()
    #bpsg = solver.solve(ssp)
    
test_basicSolve()


