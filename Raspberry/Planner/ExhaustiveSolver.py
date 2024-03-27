from Raspberry.Planner.Solution import BestSubGraph
from Raspberry.Planner.Hypothetical import Retrospection
import numpy as np
import copy

class Exhaustive:

    def solve(solver, problem, s0=0, bpsg=None) -> BestSubGraph:
        # Creates a complete state-space graph via Depth-First-Search.
        # Compares every policy with hypothetical retrospection.
        # Returns result.

        # Generate all states in problem via DFS
        policies = solver.DepthFirstSearch(problem, s0, {})
        policyPaths = []
        for pi in policies:
            policyPaths.append(solver.buildPolicyPaths(problem, pi))

        nonAccept = Retrospection.RetrospectPaths(alternatives=policyPaths)
        minIdx = np.argmin(nonAccept)
        return policies[minIdx]

    def DepthFirstSearch(solver, ssp, stateInd, colours):
        colours[stateInd] = 'v'
        piList = []
        for a in ssp.getActions(ssp.states[stateInd]):
            localPiList = [{stateInd:a}]
            for child in ssp.getActionSuccessors(ssp.states[stateInd], a):
                childColour = colours.setdefault(child.targetState.id, 'u')
                if childColour == 'u':
                    newPiList = solver.DepthFirstSearch(ssp,child.targetState.id, colours)
                    newIntegratePolicies = []
                    for idx, c in enumerate(newPiList):
                        if idx==0:
                            for p in localPiList:
                                p.update(c)
                        else:
                            for p in localPiList:
                                n = copy.deepcopy(p)
                                n.update(c)
                                newIntegratePolicies.append(n)
                    localPiList.extend(newIntegratePolicies)
            piList.extend(localPiList)

        if len(piList)==0:
            return [{}]
        return piList

    # Return every path (list of Successor objs) achievable with a policy
    def buildPolicyPaths(solver, problem, pi:dict):
        pass


