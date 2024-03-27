from Raspberry.Environment.GeneralMDP import MDP
from Raspberry.Environment.Result import AttackResult
from Raspberry.Planner.Solution import BestSubGraph
import numpy as np

class Retrospection:
 
    def Retrospect(ssp:MDP, state:MDP.State, actions:list, actionSuccessors:list, V=None):
        nonAcceptability = [0] * len(actions)
        for i in range(len(actions)):
            oneAction, oneSuccessors = actions[i], actionSuccessors[i]
            for j in range(i+1, len(actions)):
                twoAction, twoSuccessors = actions[j], actionSuccessors[j]
                if V is None:
                    oneNonAccept, twoNonAccept = Retrospection.__ArgumentPathPair(ssp, oneSuccessors, twoSuccessors)
                else:
                    oneNonAccept, twoNonAccept = Retrospection.__ArgumentPair(ssp, V, state, oneAction, oneSuccessors, twoAction, twoSuccessors)
                nonAcceptability[i]+= oneNonAccept
                nonAcceptability[j]+= twoNonAccept
        return nonAcceptability
    

    
    def __ArgumentPair(ssp:MDP, V:list, state:MDP.State, oneAction, oneSuccessors, twoAction, twoSuccessors):
        oneNonAccept, twoNonAccept = 0,0

        # Critical Question 2: Check for Defence (compare actions)
        oneExpectation = ssp.ActionExpectation(state, V, successors=oneSuccessors)
        twoExpectation = ssp.ActionExpectation(state, V, successors=twoSuccessors)
        result, t = ssp.CompareExpectations(oneExpectation, twoExpectation)

        oneVulnerable, twoVulnerable = Retrospection.vulnerable(result)

        # Critical Question 1: Check for inequality (compare arguments/successors)
        for oneSuccessor in oneSuccessors:
            for twoSuccessor in twoSuccessors:
                oneE = ssp.SuccessorExpectation(V, state, oneAction, oneSuccessor)
                twoE = ssp.SuccessorExpectation(V, state, twoAction, twoSuccessor)
                cq1, t = ssp.CompareExpectations(oneE, twoE)
                
                # Track Attacker and Defender Non Acceptability
                if cq1==AttackResult.ATTACK:
                    twoNonAccept += twoSuccessor.probability*twoVulnerable
                elif cq1==AttackResult.REVERSE:
                    oneNonAccept += oneSuccessor.probability*oneVulnerable
        
            
        # When 'trap theory or above' does have influence, trap not in effect. Return normal
        # Or when not in a trap ,return normal:
        return oneNonAccept, twoNonAccept


    def vulnerable(result):
        vOne, vTwo = 1, 1 # 1 means vulnerable; 0 means cannot be attacked (defended)
        if result==AttackResult.ATTACK:
            vOne = 0 # Attack arguments cannot be attacked
        elif result==AttackResult.REVERSE:
            vTwo = 0 # Defender arguments cannot be attacked
        elif result==AttackResult.ABSOLUTE_ATTACK:
            return 0, 1 # Automatic attack on all defender arguments
        elif result==AttackResult.ABSOLUTE_REVERSE:
            return 1, 0 # Automatic attack on all attacker arguments
        return vOne, vTwo


    def __ArgumentPathPair(ssp:MDP, onePaths, twoPaths):
        oneProbability = [s.probability for s in onePaths]
        twoProbability = [s.probability for s in twoPaths]

        # Critical Question 2: Check for difference of expectation
        oneExpectation = ssp.ManyPathsExpectation(onePaths, oneProbability)
        twoExpectation = ssp.ManyPathsExpectation(twoPaths, twoProbability)
        result, t = ssp.CompareExpectations(oneExpectation, twoExpectation)
        oneVulnerable, twoVulnerable = Retrospection.vulnerable(result)

        # Critical Question 1: Check for inequality (compare arguments/successors)
        for oneIdx, oneP in enumerate(onePaths):
            for twoIdx, twoP in enumerate(twoPaths):
                oneE = ssp.PathExpectation(oneP)
                twoE = ssp.PathExpectation(twoP)
                cq1, t = ssp.CompareExpectations(oneE, twoE)
                
                # Track Attacker and Defender Non Acceptability
                if cq1==AttackResult.ATTACK:
                    twoNonAccept += twoProbability[twoIdx]*twoVulnerable
                elif cq1==AttackResult.REVERSE:
                    oneNonAccept += oneProbability[oneIdx]*oneVulnerable


