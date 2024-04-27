from Raspberry.Planner.MDP_Solvers.HumanSolver import Solver
from Raspberry.Planner.MDP_Solvers.MM_ValueIteration import Multi_ValueIteration
from Raspberry.Environment.Abstract.AbstractProblem import AbstractProblem
import Raspberry.Environment.Abstract.AbstractGenerator as ag
from Raspberry.Environment.TeacherBot.Problem import MultiTeacherBot

#d = ag.setupFunctionFromFile('test/SavedAbstractEnvs/probDoubleAction.json')

ssp = MultiTeacherBot()
solver = Solver()
bpsg = solver.solve(ssp)
print('')

