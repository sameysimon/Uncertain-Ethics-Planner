# Value Iteration Implementation to solver a Singleton-Moral MDP with Hypothetical Retrospection

from EthicsPlanner.Environment.Result import AttackResult
from EthicsPlanner.Environment.MultiMoralMDP import MM_MDP
import numpy as np
import copy

class Singleton_ValueIteration():
    updateCount=0

    def solve(solver, mdp:MM_MDP, theoryTag='utility') -> dict:
        if not mdp.makeAllStatesExplicit():
            print('Problem is too large to be solved with Value Iteration.')
            return {}
        solver.revisions=0
        converged=False
        theory=mdp.getTheoryByTag(theoryTag)

        # Initialise valuation function/all states
        E = {}
        for s in mdp.states:
            Singleton_ValueIteration.appendToE(E, mdp.EmptyValuation())
            
        pi={}
        while not converged:
            E_ = copy.deepcopy(E)
            for s in mdp.states:
                actions = mdp.getActions(s)
                if len(actions)==0:
                    continue
                actionEstimates = solver.actionEstimates(s, actions, mdp, theory, E_)
                bestActionIdx = solver.idxPreferred(actionEstimates, theory)
                mdp.setValuation(E,s,actions[bestActionIdx])
                solver.revisions+=1

            converged = mdp.isConverged(E, E_, theories=[theory])
        
        # Extract Policy
        for s in mdp.states:
            actions = mdp.getActions(s)
            if len(actions)==0:
                continue
            actionEstimates = solver.actionEstimates(s, actions, mdp, theory, E_)
            bestActionIdx = solver.idxPreferred(actionEstimates, theory)
            pi[s.id] = mdp.getActions(s)[bestActionIdx]
        
        solver.V=E
        return pi

    def actionEstimates(solver, state, actions, mdp, theory, E):
        l = [] 
        for a in actions:
            estimate = mdp.EmptyValuation()
            l.append(estimate)
            successors = mdp.getActionSuccessors(state, a)
            for t in mdp.Theories:
                estimate[t.tag] = theory.Gather(successors, E[t.tag])
        return l

    def idxPreferred(solver, l, theory):
        argMax = 0
        for eIdx in range(1, len(l)):
            if theory.CompareEstimates(l[argMax][theory.tag], l[eIdx][theory.tag])==AttackResult.REVERSE:
                argMax = eIdx
        return argMax

    def appendToE(E, theoryValues:dict):
        for tag, value in theoryValues.items():
            E.setdefault(tag,[]).append(value)
