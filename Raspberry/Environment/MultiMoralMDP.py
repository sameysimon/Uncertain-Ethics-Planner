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

    def SuccessorExpectation(self, V, state, action, successor) -> dict:
        # Returns:
        #   Expectation (dict) Returns a expected moral value on a successor of action.
        expect = self.EmptyValuation()
        t:MoralTheory
        for C in self.TheoryClasses:
            for tag in C:
                t=self.getTheoryByTag(tag)
                expect[tag] = t.Gather([successor], V[tag],probabilities=[1])
        return expect

    def ActionExpectation(self, state, V, action=0, successors=0) -> dict:
        # Returns:
        #   Expectation (dict) Returns a expected moral values from an action.
        if successors==0:
            successors = self.getActionSuccessors(state, action)

        expect = self.EmptyValuation()
        for C in self.TheoryClasses:
            for tag in C:
                t=self.getTheoryByTag(tag)
                expect[t.tag] = t.Gather(successors, V[t.tag])
        return expect

    def CompareExpectations(self, expectOne, expectTwo, maxClass=None) -> tuple:
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
            for tag in C:
                t=self.getTheoryByTag(tag)
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

    def EmptyValuation(self) -> dict:
        v = {}
        for t in self.Theories:
            v[t.tag] = t.EmptyEstimate()
        return v

    def getStateHeuristic(self, state: MDP.State) -> dict:
        h = {}
        for t in self.Theories:
            h[t.tag] = t.StateHeuristic(state)
        return h
    
    # Update the valuation of state in V to match the successors of action
    def setValuation(self, V, state, action) -> dict:
        successors = self.getActionSuccessors(state, action)
        for t in self.Theories:
            V[t.tag][state.id] = t.Gather(successors, V[t.tag])
        return V

    def isConverged(self, V, V_, theories=None, epsilon=0.001) -> bool:
        if theories==None:
            theories=self.Theories
        for t in theories:
            if not t.IsConverged(V[t.tag], V_[t.tag], epsilon):
                return False
        return True
        
    def getTheoryByTag(self, tag) -> MoralTheory:
        for t in self.Theories:
            if t.tag==tag:
                return t
        return None
    