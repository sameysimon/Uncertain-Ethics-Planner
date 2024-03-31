# Singleton Moral Markov Decision Process 
from Raspberry.Environment.GeneralMDP import MDP
from Raspberry.Environment.Result import AttackResult
from Raspberry.Environment.Theory.MoralTheory import MoralTheory
from abc import ABC, abstractmethod 
import numpy as np


class MM_MDP(MDP, ABC):
        
    def __init__(self):
        super().__init__()
        self.TheoryClasses = [] # List of lists of Moral Theories: lower indexed are preferred.

    def SuccessorExpectation(self, V, state, action, successor):
        # Returns:
        #   Expectation (dict) Returns a expected moral value on a successor of action.
        expect = self.EmptyValuation()
        t:MoralTheory
        for C in self.TheoryClasses:
            for t in C:
                expect[t.tag] = t.Gather([successor], V[t.tag],probabilities=[1])
        return expect

    def ActionExpectation(self, state, V, action=0, successors=0):
        # Returns:
        #   Expectation (dict) Returns a expected moral values from an action.
        if successors==0:
            successors = self.getActionSuccessors(state, action)

        expect = self.EmptyValuation()
        for C in self.TheoryClasses:
            for t in C:
                expect[t.tag] = t.Gather(successors, V[t.tag])
        return expect

    def ManyPathsExpectation(self, state, paths, probabilities):
        for idx, p in enumerate(paths):
            paths[idx] = self.PathExpectation(p)
        expect = self.EmptyValuation()
        for C in self.TheoryClasses:
            for t in C:
                expect[t.tag] = t.EstimateUnion(t.JudgeState(state), paths, probabilities, self)
        return expect

    def PathExpectation(self, path, probability):
        j = {}
        for C in self.TheoryClasses:
            for t in C:
                for idx in range(len(path)-1):
                    j[t.tag] = t.IntegrateJudgments(t.JudgeState(path[idx].targetState), j[t.tag])

        expect = self.EmptyValuation()

        # Make the total judgement a probabilistic estimate
        for C in self.TheoryClasses:
            for t in C:
                expect[t.tag] = t.EstimateUnion(j[t.tag], [expect[t.tag]], [probability], self)

        return expect

    def CompareExpectations(self, expectOne, expectTwo, maxClass=None):
        #Returns:
        #   (AttackResult, MoralTheory) A tuple of the attack result and theory that caused attack. Theory is None in a draw.
        # Considers preferred theory classes first. If they launch attack, no need to consider rest.
        if maxClass == None:
            maxClass = len(self.TheoryClasses)-1
        if maxClass >= len(self.TheoryClasses):
            maxClass = len(self.TheoryClasses)-1
        if maxClass < 0:
            maxClass = 0

        for classIdx in range(0,maxClass+1):
            C=self.TheoryClasses[classIdx]
            final = AttackResult.DRAW
            for t in C:
                r = t.CompareEstimates(expectOne[t.tag], expectTwo[t.tag])
                if r != AttackResult.DRAW:
                    if final == AttackResult.DRAW:
                        final=r
                    elif final != AttackResult.DRAW and final != r:
                        final=AttackResult.DILEMMA
            if final != AttackResult.DRAW:
                return final,classIdx
        return AttackResult.DRAW, classIdx

# If theory class has conflict, move to next theory class.

    def EmptyValuation(self):
        v = {}
        for C in self.TheoryClasses:
            for t in C:
                v[t.tag] = t.EmptyEstimate()
        return v

    def getStateHeuristic(self, state: MDP.State) -> dict:
        h = {}
        for C in self.TheoryClasses:
            for t in C:
                h[t.tag] = t.StateHeuristic(state)
        return h
    
    # Update the valuation of state in V to match the successors of action
    def setValuation(self, V, state, action):
        successors = self.getActionSuccessors(state, action)
        for C in self.TheoryClasses:
            for t in C:
                V[t.tag][state.id] = t.Gather(successors, V[t.tag])
        return V

    def isConverged(self, V, V_, epsilon=0.001):
        for C in self.TheoryClasses:
            for t in C:
                if not t.IsConverged(V[t.tag], V_[t.tag], epsilon):
                    return False
        return True
        
