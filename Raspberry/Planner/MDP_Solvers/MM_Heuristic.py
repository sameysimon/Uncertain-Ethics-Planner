from Raspberry.Planner.Solution import BestSubGraph
from Raspberry.Planner.Hypothetical import Retrospection
from Raspberry.Planner.Log import Logger
from Raspberry.Planner.MDP_Solvers.iLAOStar import HeuristicSolver

import numpy as np
import copy
from tabulate import tabulate


class Solver(HeuristicSolver):

    # Check convergence with all theories
    def isConverged(solver, mdp, bpsg:BestSubGraph):
        V_ = copy.deepcopy(bpsg.V)
        def visitState(s):
            nonlocal mdp, bpsg
            solver.ReviseAction(s, mdp, bpsg)

        solver.DepthFirstSearch(mdp, bpsg, visitState)
        bpsg.update(mdp)
        return mdp.isConverged(bpsg.V, V_, solver.getRelevantTheories(mdp))

    # Select best action and update policy/value function
    def ReviseAction(solver, stateIndex, mdp, bpsg):
        state = mdp.states[stateIndex] # State object
        actions = mdp.getActions(state) # Executable actions

        if len(actions)==0:
            return

        # Get Non-Acceptability value for each alternative (probability of moral regret/-ve retrospection)
        actionSuccessors = [mdp.getActionSuccessors(state, a) for a in actions]
        nonAcceptability = Retrospection.Retrospect(mdp, state, actions, actionSuccessors, bpsg.V)
        
        bestActionIdx = np.argmin(nonAcceptability)
        bestAction = actions[bestActionIdx]
        
        # Update policy and Value function.
        bpsg.pi[stateIndex] = bestAction
        # Below would update V in-place.
        #mdp.setValuation(bpsg.V, mdp.states[stateIndex], bestAction)
    
    def getRelevantTheories(self, mdp):
        l=[]
        for C in mdp.TheoryClasses:
            for t in C:
                l.append(mdp.getTheoryByTag(t))
        return l