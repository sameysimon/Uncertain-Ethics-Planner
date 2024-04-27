from Raspberry.Planner.MDP_Solvers.MM_Heuristic import Solver
from Raspberry.Planner.MDP_Solvers.iLAOStar import HeuristicSolver
import Raspberry.Environment.Abstract.AbstractGenerator as ag
from Raspberry.Environment.TeacherBot.Problem import TeacherProblem
from Raspberry.Environment.TeacherBot.Utilitarian import EducationUtility
from Raspberry.Environment.TeacherBot.Welfare import Wellbeing
from Raspberry.Environment.TeacherBot.KantCI import NoLies
import Raspberry.Environment.GraphVisualiser as v
from Log import Logger
import os
import time
import sys

if '-debug' in sys.argv:
    Logger.debug=True

mdp = TeacherProblem(theoryClasses=[[NoLies()], [EducationUtility(), Wellbeing()]])
solver = Solver()
t1 = time.process_time()
bpsg = solver.solve(mdp)
t2 = time.process_time()
print('done')

v.VisualiseSolutionGraph(mdp, bpsg)
v.VisualiseExplicitGraph(mdp, bpsg)
print('Visualised Graph at {file}/tempExpGraph.pdf'.format(file=os.getcwd()))
print('Expanded {n} states'.format(n=len(bpsg.expandedStates)))
print('Solution graph has {n} states.'.format(n=len(bpsg.states)))
print('Time taken {t}'.format(t=t2-t1))
startState = mdp.states[0]
for C in mdp.TheoryClasses:
    for t in C:
        print('{theory} final estimation={g}'.format(theory=t.tag, g=t.Gather(mdp.getActionSuccessors(startState, bpsg.pi[startState.id], readOnly=True), bpsg.V[t.tag])))
print('')

for s in bpsg.states:
    if s in bpsg.pi.keys():
        print("({id},{a})".format(id=s, a=bpsg.pi[s]))



def generateEnvironments():
    d = ag.randomTreeSetup(3, 3, 3, seed=10)
    ag.saveSetupParams('testEnv1.json', d)

    d = ag.randomTreeSetup(3, 3, 3, seed=101)
    ag.saveSetupParams('testEnv2.json', d)

    d = ag.randomTreeSetup(3, 3, 3, seed=1001)
    ag.saveSetupParams('testEnv3.json', d)

# 2 have passed deadlines; 2 are to post; 1 is to post with extended deadline, but he will email separately about that.


