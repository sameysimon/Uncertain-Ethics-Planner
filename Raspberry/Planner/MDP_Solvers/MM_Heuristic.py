from Raspberry.Planner.Solution import BestSubGraph
from Raspberry.Planner.Hypothetical import Retrospection
from Raspberry.Planner.Logger import Log
from Raspberry.Planner.MDP_Solvers.iLAOStar import HeuristicSolver

import numpy as np
import copy
from tabulate import tabulate


class Solver(HeuristicSolver):

    # Check convergence with all theories
    def isConverged(self, ssp, bpsg:BestSubGraph):
        V_ = copy.deepcopy(bpsg.V)
        def visitState(s):
            nonlocal ssp, bpsg
            self.ReviseAction(s, ssp, bpsg)

        bpsg.DepthFirstSearch(visitState)
        bpsg.update(ssp)
        return ssp.isConverged(bpsg.V, V_)

    # Select best action and update policy/value function
    def ReviseAction(solver, stateIndex, ssp, bpsg):
        state = ssp.states[stateIndex] # State object
        actions = ssp.getActions(state) # Executable actions

        if len(actions)==0:
            return

        # Get Non-Acceptability value for each alternative (probability of moral regret/-ve retrospection)
        actionSuccessors = [ssp.getActionSuccessors(state, a) for a in actions]
        nonAcceptability = Retrospection.Retrospect(ssp, state, actions, actionSuccessors, bpsg.V)
        
        bestActionIdx = np.argmin(nonAcceptability)
        bestAction = actions[bestActionIdx]

        Log.retrospection(state, actions, nonAcceptability, bestAction)
        # Update policy and Value function.
        bpsg.pi[stateIndex] = bestAction
        ssp.setValuation(bpsg.V, ssp.states[stateIndex], bestAction)
