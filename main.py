from Raspberry.Planner.MDP_Solvers.MM_ValueIteration import Multi_ValueIteration as VI
from Raspberry.Planner.MDP_Solvers.MM_Heuristic import Solver
import Raspberry.Environment.Abstract.AbstractGenerator as ag
from Raspberry.Environment.TeacherBot.Problem import MultiTeacherBot
import Raspberry.Environment.GraphVisualiser as v




mdp = MultiTeacherBot()
solver = Solver()
bpsg = solver.solve(mdp)
v.VisualiseExplicitGraph(mdp, bpsg, 'tempExpGraph')



def generateEnvironments():
    d = ag.randomTreeSetup(3, 3, 3, seed=10)
    ag.saveSetupParams('testEnv1.json', d)

    d = ag.randomTreeSetup(3, 3, 3, seed=101)
    ag.saveSetupParams('testEnv2.json', d)

    d = ag.randomTreeSetup(3, 3, 3, seed=1001)
    ag.saveSetupParams('testEnv3.json', d)

# 2 have passed deadlines; 2 are to post; 1 is to post with extended deadline, but he will email separately about that.
