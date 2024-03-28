# Singleton Moral Markov Decision Process 
from Raspberry.Environment.GeneralMDP import MDP
from Raspberry.Environment.Result import AttackResult
from Raspberry.Environment.Theory.MoralTheory import MoralTheory
from abc import ABC, abstractmethod 
import numpy as np


class MM_MDP(MDP, ABC):
        
    def __init__(self):
        super().__init__()

    def SuccessorExpectation(self, V, state, action, successor):
        # Returns:
        #   Expectation (dict) Returns a expected moral value on a successor of action.
        expect = self.EmptyValuation()
        t:MoralTheory
        for t in self.Theories:
            expect[t.tag] = t.Gather([successor], V[t.tag],probabilities=[1])
        return expect

    def ActionExpectation(self, state, V, action=0, successors=0):
        # Returns:
        #   Expectation (dict) Returns a expected moral values from an action.
        if successors==0:
            successors = self.getActionSuccessors(state, action)

        expect = self.EmptyValuation()
        for t in self.Theories:
            expect[t.tag] = t.Gather(successors, V[t.tag])
        return expect

    def ManyPathsExpectation(self, state, paths, probabilities):
        for idx, p in enumerate(paths):
            paths[idx] = self.PathExpectation(p)
        expect = self.EmptyValuation()
        for t in self.Theories:
            expect[t.tag] = t.EstimateUnion(t.JudgeState(state), paths, probabilities, self)
        return expect

    def PathExpectation(self, path, probability):
        j = {}
        for t in self.Theories:
            for idx in range(len(path)-1):
                j[t.tag] = t.IntegrateJudgments(t.JudgeState(path[idx].targetState), j[t.tag])
        expect = self.EmptyValuation()

        # Make the total judgement a probabilistic estimate
        for t in self.Theories:
            expect[t.tag] = t.EstimateUnion(j[t.tag], [expect[t.tag]], [probability], self)

        return expect

    def CompareExpectations(self, expectOne, expectTwo):
        #Returns:
        #   (AttackResult, MoralTheory) A tuple of the attack result and theory that caused attack. Theory is None in a draw.
        for t in self.Theories:
            r = t.CompareEstimates(expectOne[t.tag], expectTwo[t.tag]) 
            if r != AttackResult.DRAW:
                return r, t
        return AttackResult.DRAW, None



    def EmptyValuation(self):
        v = {}
        for t in self.Theories:
            v[t.tag] = t.EmptyEstimate()
        return v
    # Get it now lmao
    # HERE!!!!!!
    def getStateHeuristic(self, state: MDP.State) -> dict:
        h = {}
        for t in self.Theories:
            h[t.tag] = t.StateHeuristic(state)
        return h
    
    # Update the valuation of state in V to match the successors of action
    def setValuation(self, V, state, action):
        successors = self.getActionSuccessors(state, action)
        for t in self.Theories:
            V[t.tag][state.id] = t.Gather(successors, V[t.tag])

    def isConverged(self, V, V_, epsilon=0.001):
        for t in self.Theories:
            if not t.IsConverged(V[t.tag], V_[t.tag], epsilon):
                return False
        return True
        
