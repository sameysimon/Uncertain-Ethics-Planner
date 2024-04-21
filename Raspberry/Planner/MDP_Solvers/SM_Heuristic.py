from Raspberry.Planner.Solution import BestSubGraph
from Raspberry.Planner.Hypothetical import Retrospection
from Raspberry.Planner.Logger import Log
from Raspberry.Planner.MDP_Solvers.iLAOStar import HeuristicSolver
from Raspberry.Environment.Result import AttackResult
import numpy as np
import copy



class Singleton_HeuristicSolver(HeuristicSolver):
    
    def isConverged(self, mdp, bpsg:BestSubGraph):
        V_ = copy.deepcopy(bpsg.V[self.theory.tag])
        def visitState(s):
            nonlocal mdp, bpsg
            self.ReviseAction(s, mdp, bpsg)
        bpsg.DepthFirstSearch(visitState)
        bpsg.update(mdp)
        return self.theory.IsConverged(bpsg.V[self.theory.tag], V_)

    def solve(solver, mdp, s0=0, bpsg=None, theoryTag='utility') -> BestSubGraph:
        if bpsg==None:
            bpsg=BestSubGraph(startStateIndex=s0, ssp=mdp)
        solver.theory=mdp.getTheoryByTag(theoryTag)
        converged=False
        i=0
        while not converged and i < 1000:
            bpsg = solver.FindAndRevise(mdp, bpsg)
            converged = solver.isConverged(mdp, bpsg)
            i+=1
        
        return bpsg

    # Select best action and update policy/value function
    def ReviseAction(solver, stateIndex, mdp, bpsg):
        state = mdp.states[stateIndex] # State object
        actions = mdp.getActions(state) # Executable actions

        if len(actions)==0:
            return

        values = []
        for a in actions:
            r=0
            successors = mdp.getActionSuccessors(state, a)
            values.append(solver.theory.Gather(successors, bpsg.V[solver.theory.tag]))

        bestActionIdx = 0 # Default best action is the first.
        # Linear scan for best action
        for actionIdx, val in enumerate(values):
            if solver.theory.CompareEstimates(val, values[bestActionIdx])==AttackResult.ATTACK:
                bestActionIdx = actionIdx
        
        # Update policy and Value function.
        bestAction = actions[bestActionIdx]
        bpsg.pi[stateIndex] = bestAction
        mdp.setValuation(bpsg.V, mdp.states[stateIndex], bestAction)
        
