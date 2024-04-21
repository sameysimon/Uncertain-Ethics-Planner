from Raspberry.Planner.Solution import BestSubGraph
from Raspberry.Planner.Hypothetical import Retrospection
import numpy as np
class Solver:
    def solve(solver, problem, s0=0, bpsg=None):
        if bpsg==None:
            bpsg=BestSubGraph(startStateIndex=s0, ssp=problem)
        
        solver.FindAndRevise(problem, bpsg)
        return bpsg

    def FindAndRevise(solver, mdp, bpsg) -> BestSubGraph:
        isUnexpandedStates = True
        while isUnexpandedStates:
            # Run visitState on all states in Depth-First, post-order fashion.
            def visitState(stateInd, probability):
                nonlocal mdp, bpsg
                state = mdp.states[stateInd]
                if not stateInd in bpsg.expandedStates:
                    newStates = mdp.expandState(mdp.states[stateInd])
                    bpsg.updateValuation(mdp, newStates) # Inits heuristic for new states
                print('StateID: ' + str(stateInd))
                print('State Props:' + str(state.props))
                print('**')
                actions = mdp.getActions(state)
                actionSuccessors = [mdp.getActionSuccessors(state,a) for a in actions]
                nonAcceptability = Retrospection.Retrospect(mdp, state, mdp.getActions(state), actionSuccessors, bpsg.V)
                bestActionIdx = np.argmin(nonAcceptability)
                print('HR Chooses Action ' + str(actions[bestActionIdx]))
                print('Retrospection File Generated.')
                i=''
                while i!='q':
                    print('ACTIONS: ' + str(actions))
                    i = input('Choose one by typing it. q to move on.')
                    if not (i in actions):
                        continue
                    for s in mdp.getActionSuccessors(state, i):    
                        print("Probability: " + str(s.probability))
                        print('Target ID: ' + str(s.targetState.id))
                        print('Target Props: ' + str(s.targetState.props))
                        n = input('Enter to continue; q to skip')
                        if n == 'q':
                            break       
                    print()
                while True:
                    a = input('Choose an action by typing it')
                    if not a in actions:
                        continue
                    bpsg.pi[stateInd] = a
                    bpsg.update(mdp)
                    break


            # Revise policy in depth-first-search
            solver.DepthFirstSearch(mdp, bpsg, visitState)
            # update solution graph to match policy
            bpsg.update(mdp)
            # Check for more unexpanded states in solution graph
            isUnexpandedStates = len(bpsg.getUnexpandedStatesInBPSG(mdp)) > 0

        # Return solution graph result, and non-acceptability of solution
        return bpsg



    def DepthFirstSearch(solver, mdp, bpsg, onVisitFn):
        def visit(stateInd, colours, p, fn=None):
            colours[stateInd] = 'v'
            if stateInd in bpsg.pi.keys():
                for s in mdp.getActionSuccessors(mdp.states[stateInd], bpsg.pi[stateInd]):
                    childColour = colours.setdefault(s.targetState.id, 'u')
                    if childColour == 'u':
                        visit(s.targetState.id, colours, p*s.probability, fn)
            if fn:
                fn(stateInd, p)
            
        colours = {}
        visit(0,colours, 1, onVisitFn)