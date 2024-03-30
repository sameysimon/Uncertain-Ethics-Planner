from Raspberry.Planner.MM_FindRevise import Solver as FR
from Raspberry.Planner.SM_ValueIteration import Solver as VI
import Raspberry.Environment.Abstract.AbstractGenerator as ag

from Raspberry.Environment.Abstract.AbstractProblems import AbstractWorld_MM_SSP as MMSSP
from Raspberry.Environment.Abstract.AbstractProblems import AbstractWorld_SM_MDP as SMMDP


setup = ag.randomTreeSetup(maxBranchFactor=3, maxActionFactor=3, depth=3, seed=101)

FRssp = MMSSP(setup=setup)
solver = FR()
bpsg = solver.solve(FRssp)
frPi = bpsg.pi

FRtileToAction = {}
for FRsID, FRaction in frPi.items():
    FRtileToAction[FRssp.states[FRsID].props['tile']] = FRaction

VIssp = SMMDP(setup=setup)
solver = VI()
viPi = solver.solve(VIssp)

VItileToAction = {}
for VIsID, VIaction in viPi.items():
    VItileToAction[VIssp.states[VIsID].props['tile']] = VIaction

for tile, action in FRtileToAction.items():
    if VItileToAction[tile]!= action:
        print('Different on tile ' + str(tile))

print('finished')