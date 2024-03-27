from Raspberry.Planner.Solution import BestSubGraph
from Raspberry.Planner.Hypothetical import Retrospection
import numpy as np
import copy

class Solver:
    updateCount=0
    def isConverged(self, ssp, bpsg:BestSubGraph):

        V_ = copy.deepcopy(bpsg.V)
        def visitState(s):
            nonlocal ssp, bpsg
            if ssp.isGoal(ssp.states[s]):
                return
            self.ReviseAction(s, ssp, bpsg)

        bpsg.DepthFirstSearch(visitState)
        bpsg.update(ssp)
        return ssp.isConverged(bpsg.V, V_)

    def solve(solver, problem, s0=0, bpsg=None) -> BestSubGraph:
        if bpsg==None:
            bpsg=BestSubGraph(startStateIndex=s0, ssp=problem)
        converged=False
        i=0
        while not converged and i < 1000:
            bpsg = solver.FindAndRevise(problem, bpsg)
            converged = solver.isConverged(problem, bpsg)
            i+=1
        
        return bpsg

    def FindAndRevise(solver, ssp, bpsg) -> BestSubGraph:
        isUnexpandedStates = True
        while isUnexpandedStates:
            # Run visitState on all states in Depth-First, post-order fashion.
            def visitState(stateInd, probability):
                nonlocal ssp, bpsg
                if not ssp.isGoal(ssp.states[stateInd]) and not (stateInd in bpsg.expandedStates):
                    bpsg.expandedStates.append(stateInd)
                    newStates = ssp.expandState(ssp.states[stateInd])
                    bpsg.updateValuation(ssp, newStates) # Inits heuristic for new states
                # Select and set best action in policy/value function
                solver.ReviseAction(stateInd, ssp, bpsg)
                #ssp.VisualiseExplicitGraph(bpsg, fileName='temp/update'+str(Solver.updateCount))
                Solver.updateCount+=1
                
            # Revise policy in depth-first-search
            solver.DepthFirstSearch(ssp, bpsg, visitState)
            # update solution graph to match policy
            bpsg.update(ssp)
            # Check for more unexpanded states in solution graph
            isUnexpandedStates = len(bpsg.getUnexpandedStatesInBPSG(ssp)) > 0

        # Return solution graph result, and non-acceptability of solution
        return bpsg

    # Select best action and update policy/value function
    def ReviseAction(solver, stateIndex, ssp, bpsg):
        state = ssp.states[stateIndex] # State object
        actions = ssp.getActions(state) # Executable actions

        if len(actions)==0:
            return

        # Get Non-Acceptability value for each alternative (probability of moral regret/-ve retrospection)
        actionSuccessors = [ssp.getActionSuccessors(state, a) for a in actions]
        nonAcceptability = Retrospection.Retrospect(ssp, state, actions, actionSuccessors, bpsg.V)
        
        lowestNonAccept = min(nonAcceptability)
        ethicalActions = []
        for idx, a in enumerate(actions):
            if nonAcceptability[idx]==lowestNonAccept:
                ethicalActions.append(a)


        # Select ethical action with best reward
        reward = []
        for action in ethicalActions:
            r = ssp.Reward(state, action)
            for successor in ssp.getActionSuccessors(state, action):
                r += successor.probability * bpsg.V[state.id]['reward']
            reward.append(r)
        bestIdx = np.argmax(reward)
        bestAction = ethicalActions[bestIdx]

        # Update policy and Value function.
        bpsg.pi[stateIndex] = bestAction
        ssp.setValuation(bpsg.V, ssp.states[stateIndex], bestAction)


    def DepthFirstSearch(solver, ssp, bpsg, onVisitFn):
        def visit(stateInd, colours, p, fn=None):
            colours[stateInd] = 'v'
            if stateInd in bpsg.pi.keys():
                for s in ssp.getActionSuccessors(ssp.states[stateInd], bpsg.pi[stateInd]):
                    childColour = colours.setdefault(s.targetState.id, 'u')
                    if childColour == 'u':
                        visit(s.targetState.id, colours, p*s.probability, fn)
            if fn:
                fn(stateInd, p)
            
        colours = {}
        visit(0,colours, 1, onVisitFn)
