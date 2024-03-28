# Value Iteration Implementation to solver a Singleton Moral MDP

from Raspberry.Environment.Result import AttackResult
from Raspberry.Planner.Hypothetical import Retrospection
from Raspberry.Environment.SingletonMoralMDP import SM_MDP
import numpy as np
import copy

class Solver:
    updateCount=0


    def solve(solver, problem:SM_MDP) -> dict:
        if not problem.makeAllStatesExplicit():
            print('Problem is too large to be solved with Value Iteration.')
            return {}

        converged=False
        i=0
        E = []*len(problem.states)
        while not converged:
            E_ = copy.deepcopy(E)
            for s in problem.states:
                l = solver.actionEstimates(s,problem, E)
                E[s.id] = solver.preferred(l,problem.Theory)
            converged = problem.Theory.isConverged(E, E_)
        pi={}
        for s in problem.states:
            pi[s.id] = problem.getActions(s)[solver.idxPreferred(l, problem.Theory)]
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