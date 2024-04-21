# Value Iteration Implementation to solver a Singleton Moral MDP

from Raspberry.Environment.Result import AttackResult
from Raspberry.Environment.MultiMoralMDP import MM_MDP
from Raspberry.Planner.MDP_Solvers.ValueIteraton import ValueIteration
import numpy as np
import copy

class Singleton_ValueIteration(ValueIteration):
    updateCount=0

    def __init__(self, theoryTag='utility') -> None:
        super().__init__()
        self.tag = theoryTag

    def updateStateEvaluation(solver, state, problem, F):
        # Updates an estimate function to equal the optimal estimate.
        actions = problem.getActions(state)
        if len(actions)==0:
            return F[state.id]
        actionEstimates = solver.__allActionEstimates(state, problem,actions, F)
        return solver.__preferredEstimate(actionEstimates, problem.getTheoryByTag(solver.tag))

    def IsConverged(solver, problem:MM_MDP, F, F_):
        return problem.getTheoryByTag(solver.tag).IsConverged(F,F_)

    def __allActionEstimates(solver, state, problem, actions, F):
        l = []
        for a in actions:
            successors = problem.getActionSuccessors(state, a)
            l.append(problem.getTheoryByTag(solver.tag).Gather(successors, F))
        return l

    def __preferredEstimate(solver, estimates, theory):
        return estimates[solver.__idxPreferred(estimates, theory)]

    def getPreferredAction(solver, state, problem, F):
        # given an estimate function over states, finds the maximally accepted action
        actions = problem.getActions(state)
        l = solver.__allActionEstimates(state,problem, actions, F)
        if len(actions)!=0:
            return actions[solver.__idxPreferred(l, problem.getTheoryByTag(solver.tag))]
        return None


    def __idxPreferred(solver, l, theory):
        argMax = 0
        for eIdx in range(1, len(l)):
            if theory.CompareEstimates(l[argMax], l[eIdx])==AttackResult.REVERSE:
                argMax = eIdx
        return argMax