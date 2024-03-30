# Value Iteration Implementation to solver a Multi-Moral MDP with Hypothetical Retrospection

from Raspberry.Environment.Result import AttackResult
from Raspberry.Planner.Hypothetical import Retrospection
from Raspberry.Environment.MultiMoralMDP import MM_MDP
import numpy as np
import copy

class Solver:
    updateCount=0

    def solve(solver, problem:MM_MDP) -> dict:
        if not problem.makeAllStatesExplicit():
            print('Problem is too large to be solved with Value Iteration.')
            return {}

        converged=False
        i=0
        E = {}
        for s in problem.states:
            Solver.appendToE(E, problem.EmptyValuation())
        pi={}
        while not converged:
            E_ = copy.deepcopy(E)
            for s in problem.states:
                actions = problem.getActions(s)
                actionSuccessors = [problem.getActionSuccessors(s,a) for a in actions]
                nonAcceptability = Retrospection.Retrospect(problem, s, actions, actionSuccessors, E)
                bestAction = actions[np.argmin(nonAcceptability)]
                pi[s.id]=bestAction
                problem.setValuation(E,s,bestAction)
            converged = problem.isConverged(E, E_)
        
        return pi

    def actionEstimates(solver, state, problem, E):
        l = []
        actions = problem.getActions(state)
        for a in actions:
            successors = problem.getActionSuccessors(state, a)
            l.append(problem.Theory.Gather(successors, E))
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
