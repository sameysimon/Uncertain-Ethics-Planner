# Value Iteration Implementation to solver a Multi-Moral MDP with Hypothetical Retrospection

from EthicsPlanner.Environment.Result import AttackResult
from EthicsPlanner.Environment.MultiMoralMDP import MM_MDP
from EthicsPlanner.Planner.Hypothetical import Retrospection
import numpy as np
import copy

class Multi_ValueIteration():
    updateCount=0

    def solve(solver, mdp:MM_MDP) -> dict:
        if not mdp.makeAllStatesExplicit():
            print('Problem is too large to be solved with Value Iteration.')
            return {}
        solver.revisions=0
        converged=False
        i=0
        E = {}
        for s in mdp.states:
            Multi_ValueIteration.appendToE(E, mdp.EmptyValuation())
        pi={}
        while not converged:
            E_ = copy.deepcopy(E)
            for s in mdp.states:
                actions = mdp.getActions(s)
                if len(actions)==0:
                    continue
                actionSuccessors = [mdp.getActionSuccessors(s,a) for a in actions]
                nonAcceptability = Retrospection.Retrospect(mdp, s, actions, actionSuccessors, E_) # If passing E, then updating in-place
                solver.revisions+=1
                bestAction = actions[np.argmin(nonAcceptability)]
                pi[s.id]=bestAction
                mdp.setValuation(E,s,bestAction)
            converged = mdp.isConverged(E, E_,theories=solver.getRelevantTheories(mdp))
        solver.V=E
        return pi

    def actionEstimates(solver, state, mdp, E):
        l = []
        actions = mdp.getActions(state)
        for a in actions:
            successors = mdp.getActionSuccessors(state, a)
            l.append(mdp.Theory.Gather(successors, E))
        return l

    def preferred(solver, l, theory):
        return l[solver.argPreferred(l, theory)]

    def idxPreferred(solver, l, theory):
        argMax = 0
        for eIdx in range(1, len(l)):
            if theory.CompareEstimates(l[argMax], l[eIdx])==AttackResult.REVERSE:
                argMax = eIdx
        return argMax

    def appendToE(E, theoryValues:dict):
        for tag, value in theoryValues.items():
            E.setdefault(tag,[]).append(value)

    def getRelevantTheories(solver, mdp:MM_MDP):
        l=[]
        for C in mdp.TheoryClasses:
            for t in C:
                l.append(mdp.getTheoryByTag(t))
        return l