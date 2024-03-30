from Raspberry.Environment.GeneralMDP import MDP
from Raspberry.Environment.Result import AttackResult
from Raspberry.Planner.Solution import BestSubGraph
import numpy as np

class Retrospection:
 
    def Retrospect(ssp:MDP, state:MDP.State, actions:list, actionSuccessors:list, V=None):
        attackedArgs = [set()] * len(actions)
        for i in range(len(actions)):
            oneAction, oneSuccessors = actions[i], actionSuccessors[i]
            for j in range(i+1, len(actions)):
                twoAction, twoSuccessors = actions[j], actionSuccessors[j]
                if V is None:
                    oneAttacked, twoAttacked = Retrospection.__ArgumentPathPair(ssp, oneSuccessors, twoSuccessors)
                    attackedArgs[i].union(oneAttacked)
                    attackedArgs[j].union(twoAttacked)
                else:
                    oneAttacked, twoAttacked = Retrospection.__ArgumentPair(ssp,V,state,oneAction,oneSuccessors,twoAction,twoSuccessors)
                    attackedArgs[i]=attackedArgs[i].union(oneAttacked)
                    attackedArgs[j]=attackedArgs[j].union(twoAttacked)
                    
        nonAcceptability = []
        for attackedSet in attackedArgs:
            na = Retrospection.GetAttackProbability(attackedSet)
            nonAcceptability.append(na)
        
        return nonAcceptability
    
    def GetAttackProbability(attackedSuccessors):
        p = 0
        for s in attackedSuccessors:
            p+=s.probability
        return p

    
    def __ArgumentPair(ssp:MDP, V:list, state:MDP.State, oneAction, oneSuccessors, twoAction, twoSuccessors):
        oneAttacked, twoAttacked = set(), set()

        # Critical Question 2: Check for Defence (compare actions)
        oneExpectation = ssp.ActionExpectation(state, V, successors=oneSuccessors)
        twoExpectation = ssp.ActionExpectation(state, V, successors=twoSuccessors)
        result, t = ssp.CompareExpectations(oneExpectation, twoExpectation)

        # 0 indicates the argument is NOT vulnerable to attack; 1 means it is!
        oneActVul, twoActVul = Retrospection.vulnerable(result)
        oneVulnerable = [oneActVul]*len(oneSuccessors)
        twoVulnerable = [twoActVul]*len(twoSuccessors)

        # Critical Question 1: Check for inequality (compare arguments/successors)
        for oneIdx, oneSuccessor in enumerate(oneSuccessors):
            for twoIdx, twoSuccessor in enumerate(twoSuccessors):
                oneE = ssp.SuccessorExpectation(V, state, oneAction, oneSuccessor)
                twoE = ssp.SuccessorExpectation(V, state, twoAction, twoSuccessor)
                cq1, t = ssp.CompareExpectations(oneE, twoE)

                # Track Attacker and Defender Non Acceptability
                if cq1==AttackResult.ATTACK and twoActVul==1:
                    twoAttacked.add(twoSuccessor)
                elif cq1==AttackResult.REVERSE and oneActVul==1:
                    oneAttacked.add(oneSuccessor)
        
            
        # When 'trap theory or above' does have influence, trap not in effect. Return normal
        # Or when not in a trap ,return normal:
        return oneAttacked, twoAttacked


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


