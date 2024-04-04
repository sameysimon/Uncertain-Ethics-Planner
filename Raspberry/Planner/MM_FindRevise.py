from Raspberry.Planner.Solution import BestSubGraph
from Raspberry.Planner.Hypothetical import Retrospection
import numpy as np
import copy
from tabulate import tabulate


class Log:
    messages=[]
    cycle=0
    active=False
    def retrospection(state, actions, nonaccept, bestAction):
        if Log.active==False:
            return
        m="For state {s}, there are {l} ethical actions:\n".format(l=len(actions), s=state.id)
        for idx, a in enumerate(actions):
            m+= "   Action {a} with {n} non-acceptability".format(a=a,n=nonaccept[idx])
            if a==bestAction:
                m+= "*"
            m+="\n"
        m+= "Selected action {a}".format(a=bestAction)
        Log.__addToLog(m)
    
    def EstimateMatrix(E, showStates=[]):
        if Log.active==False:
            return
        m="\After Cycle {c}, Updated values in Estimate Matrix:\n".format(c=Log.cycle)
        table = {}
        for key in E:
            table[key] = [E[key][index] for index in showStates]

        m += tabulate(table,headers="keys", tablefmt="grid", showindex=True)
        Log.__addToLog(m)
        
    def NegativeHR(state, action, attackingAction, attacks):
        if Log.active==False:
            return
        m = "Negative retrospection for action {a} on state {s}.\n".format(state.id,action)
        m+= "Should take {aa} because: \n".format(attackingAction)
        for sourceSuccessor, targetSuccessor in attacks:
            m+= "   If we reach: {targetID} with probability {p}, \n".format(targetID=targetSuccessor.targetState.id, p=targetSuccessor.probability)
            m+= "   Then we miss: {sourceID} with probability {p} \n".format(sourceID=sourceSuccessor.targetState.id, p=sourceSuccessor.probability)
        Log.__addToLog(m)

    def VisualiseGraph(bpsg, ssp):
        if Log.active==False:
            return
        ssp.VisualiseExplicitGraph(bpsg, fileName='temp/update'+str(Log.cycle))

    def newCycle():
        if Log.active==False:
            return
        Log.cycle+=1

    def __addToLog(m):
        if Log.active==False:
            return
        Log.messages.append(m+"\n")

    def Flush():
        if Log.active==False:
            return
        file = open('temp/data'+str(Log.cycle)+'.txt','w')
        for m in Log.messages:
            file.write(m)
        file.close()
        Log.messages=[]


class Solver:
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

    def solve(solver, problem, s0=0, bpsg=None, makeLogs=True) -> BestSubGraph:
        Log.cycle=0
        Log.active=makeLogs
        if bpsg==None:
            bpsg=BestSubGraph(startStateIndex=s0, ssp=problem)
        converged=False
        i=0
        while not converged and i < 1000:
            bpsg = solver.FindAndRevise(problem, bpsg)
            converged = solver.isConverged(problem, bpsg)
            i+=1
        Log.Flush()
        
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
                
            # Revise policy in depth-first-search
            solver.DepthFirstSearch(ssp, bpsg, visitState)
            Log.EstimateMatrix(bpsg.V, showStates=bpsg.states)
            Log.VisualiseGraph(bpsg, ssp)
            Log.newCycle()
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
                r += successor.probability * bpsg.V['reward'][state.id]
            reward.append(r)
        bestIdx = np.argmax(reward)
        bestAction = ethicalActions[bestIdx]

        Log.retrospection(state, actions, nonAcceptability, bestAction)
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
