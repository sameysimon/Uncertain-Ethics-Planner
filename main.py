from Raspberry.Planner.MM_ValueIteration import Solver as VI
from Raspberry.Environment.ZebraCrossing.ZebraProblems import ZebraCrossing_MM_MDP

mdp = ZebraCrossing_MM_MDP()
solver=VI()
pi = solver.solve(mdp)
