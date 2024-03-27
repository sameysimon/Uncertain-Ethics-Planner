# Singleton Moral Markov Decision Process 
from Raspberry.Environment.GeneralMDP import MDP
from Raspberry.Environment.Result import AttackResult
from abc import ABC, abstractmethod 
import numpy as np


class MM_MDP(MDP, ABC):
        
    def __init__(self):
        super().__init__()

    def SuccessorExpectation(self, V, state, action, successor):
        # Returns:
        #   Expectation (dict) Returns a expected moral value on a successor of action.
        expect = self.EmptyValuation()
        for t in self.Theories:
            expect[t.tag] = t.EstimateUnion(t.JudgeState(state), [V[successor.targetState.id][t.tag]], [1], self)
        return expect

    def ActionExpectation(self, state, V, action=0, successors=0):
        # Returns:
        #   Expectation (dict) Returns a expected moral values from an action.
        if successors==0:
            successors = self.getActionSuccessors(state, action)

        expect = self.EmptyValuation()
        for t in self.Theories:
            e, p = [], []
            for s in successors:
                e.append(V[s.targetState.id][t.tag])
                p.append(s.probability)
            expect[t.tag] = t.EstimateUnion(t.JudgeState(state), e, p, self)
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

    def getStateHeuristic(self, state: MDP.State) -> dict:
        h = {}
        for t in self.Theories:
            h[t.tag] = t.StateHeuristic(state)
        return h
    
    # Update the valuation of state in V to match the successors of action
    def setValuation(self, V, state, action):
        successors = self.getActionSuccessors(state, action)
        for t in self.Theories:
            e, p = [], []
            for s in successors:
                e.append(V[s.targetState.id][t.tag])
                p.append(s.probability)
            V[state.id][t.tag] = t.EstimateUnion(t.JudgeState(state), e, p, self)
        V[state.id]['reward'] = self.Reward(state, action) + sum([s.probability*V[s.targetState.id]['reward']*self.discount for s in successors])

    def isConverged(self, V, V_, epsilon=0.001):
        for t in self.Theories:
            if not t.IsConverged(V, V_, epsilon):
                return False

        v = np.array([s['reward'] for s in V])
        v_ = np.array([s['reward'] for s in V_])

        return np.linalg.norm(v_ - v, np.inf) < epsilon
