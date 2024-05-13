from Raspberry.Planner.Solution import BestSubGraph
from Raspberry.Planner.Hypothetical import Retrospection
import numpy as np
import copy
from tabulate import tabulate

class HeuristicSolver:
    def isConverged(solver, mdp, bpsg:BestSubGraph):
        V_ = copy.deepcopy(bpsg.V)
        def visitState(s):
            nonlocal mdp, bpsg
            solver.ReviseAction(s, mdp, bpsg)

        solver.DepthFirstSearch(mdp, bpsg, visitState)
        bpsg.update(mdp)
        return mdp.isConverged(bpsg.V, V_)

    def solve(solver, mdp, s0=0, bpsg=None, cost='utility',discount=0.9) -> BestSubGraph:
        if bpsg==None:
            bpsg=BestSubGraph(startStateIndex=s0, mdp=mdp)
        solver.costTag=cost
        solver.discount=discount
        solver.revisions=0
        converged=False
        i=0
        while not converged and i < 1000:
            bpsg = solver.FindAndRevise(mdp, bpsg)

            converged = solver.isConverged(mdp, bpsg)
            if (len(bpsg.getUnexpandedStatesInBPSG(mdp)) > 0):
                converged=False
            i+=1
        
        return bpsg

    def FindAndRevise(solver, mdp, bpsg) -> BestSubGraph:
        isUnexpandedStates = True
        while isUnexpandedStates:
            # Run visitState on all states in Depth-First, post-order fashion.
            def visitState(stateInd):
                nonlocal mdp, bpsg
                if not (stateInd in bpsg.expandedStates):
                    bpsg.expandedStates.append(stateInd)
                    newStates = mdp.expandState(mdp.states[stateInd])
                    bpsg.updateValuation(mdp, newStates) # Inits heuristic for new states
                # Select and set best action in policy/value function
                solver.revisions+=1
                solver.ReviseAction(stateInd, mdp, bpsg)
                
            # Revise policy in depth-first-search
            solver.DepthFirstSearch(mdp, bpsg, visitState)
            # update solution graph to match policy
            bpsg.update(mdp)
            # Check for more unexpanded states in solution graph
            isUnexpandedStates = len(bpsg.getUnexpandedStatesInBPSG(mdp)) > 0
            # Update Valuation Function TODO 
            for idx in bpsg.pi.keys():
                mdp.setValuation(bpsg.V, mdp.states[idx], bpsg.pi[idx])

        # Return solution graph result, and non-acceptability of solution
        return bpsg

    # Select best action and update policy/value function
    def ReviseAction(solver, stateIndex, mdp, bpsg):
        state = mdp.states[stateIndex] # State object
        actions = mdp.getActions(state) # Executable actions

        if len(actions)==0:
            return

        costs = []
        costTheory = mdp.getTheoryByTag(solver.costTag)
        for a in actions:
            r=0
            successors = mdp.getActionSuccessors(state, a)
            for s in successors:
                c = costTheory.JudgeTransition(s)
                v = bpsg.V[solver.costTag][s.targetState.id]
                r += s.probability * (c + solver.discount*v)
            costs.append(r)
        
        bestActionIdx = np.argmax(costs)
        bestAction = actions[bestActionIdx]

        # Update policy and Value function.
        bpsg.pi[stateIndex] = bestAction
        #mdp.setValuation(bpsg.V, mdp.states[stateIndex], bestAction)



    def DepthFirstSearch(solver, mdp, bpsg, onVisitFn):
        def visit(stateInd, colours, fn=None):
            colours[stateInd] = 'v'
            if stateInd in bpsg.pi.keys():
                for s in mdp.getActionSuccessors(mdp.states[stateInd], bpsg.pi[stateInd]):
                    childColour = colours.setdefault(s.targetState.id, 'u')
                    if childColour == 'u':
                        visit(s.targetState.id, colours, fn)
            if fn:
                fn(stateInd)
            
        colours = {}
        visit(0,colours, onVisitFn)
