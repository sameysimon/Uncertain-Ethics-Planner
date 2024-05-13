from EthicsPlanner.Planner.Solution import BestSubGraph
from EthicsPlanner.Planner.Hypothetical import Retrospection
from EthicsPlanner.Planner.MDP_Solvers.iLAOStar import HeuristicSolver
from EthicsPlanner.Environment.Result import AttackResult
import numpy as np
import copy



class Singleton_HeuristicSolver(HeuristicSolver):
    
    def isConverged(solver, mdp, bpsg:BestSubGraph):
        V_ = copy.deepcopy(bpsg.V[solver.theory.tag])
        def visitState(s):
            nonlocal mdp, bpsg
            solver.ReviseAction(s, mdp, bpsg)
        solver.DepthFirstSearch(mdp, bpsg, visitState)
        bpsg.update(mdp)
        return solver.theory.IsConverged(bpsg.V[solver.theory.tag], V_)

    def solve(solver, mdp, s0=0, bpsg=None, theoryTag='utility') -> BestSubGraph:
        if bpsg==None:
            bpsg=BestSubGraph(startStateIndex=s0, mdp=mdp)
        solver.theory=mdp.getTheoryByTag(theoryTag)
        converged=False
        solver.revisions=0
        i=0
        while not converged and i < 1000:
            bpsg = solver.FindAndRevise(mdp, bpsg)
            converged = solver.isConverged(mdp, bpsg)
            if (len(bpsg.getUnexpandedStatesInBPSG(mdp)) > 0):
                converged=False
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
        #mdp.setValuation(bpsg.V, mdp.states[stateIndex], bestAction)
        
