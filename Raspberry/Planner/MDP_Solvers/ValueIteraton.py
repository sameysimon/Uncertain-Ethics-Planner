# Value Iteration Implementation to solver a Singleton Moral MDP

from Raspberry.Environment.Result import AttackResult
from Raspberry.Environment.MultiMoralMDP import MM_MDP
from abc import ABC, abstractmethod 
import copy

class ValueIteration(ABC):
    updateCount=0

    def solve(solver, problem:MM_MDP, cost='utility') -> dict:
        if not problem.makeAllStatesExplicit():
            print('Problem is too large to be solved with Value Iteration.')
            return {}

        converged=False
        i=0
        F = [0]*len(problem.states)
        while not converged:
            F_ = copy.deepcopy(F)
            for s in problem.states:
                F[s.id] = solver.updateStateEvaluation(s, problem, F)
            converged = solver.IsConverged(problem,F,F_)

        # Extract policy from 
        pi={}
        for s in problem.states:
            a = solver.getPreferredAction(s, problem, F)
            if a != None:
                pi[s.id] = a
        return pi


    @abstractmethod
    def IsConverged(F, F_):
        pass

    @abstractmethod
    def updateStateEvaluation(solver, state, problem, F):
        pass
    
    @abstractmethod
    def getPreferredAction(solver, state, problem, F):
        pass