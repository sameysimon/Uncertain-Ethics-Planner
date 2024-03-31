from Raspberry.Environment.MultiMoralMDP import MM_MDP
from Raspberry.Environment.Result import AttackResult
from Raspberry.Planner.Solution import BestSubGraph
import numpy as np

# Currently, only works on Multi-Moral MM_MDPs.
class Retrospection:
 
    def RetrospectPaths(ssp:MM_MDP,policyPaths:list):
        return 

    def Retrospect(ssp:MM_MDP, state:MM_MDP.State, actions:list, actionSuccessors:list, V):
        attackedArgs = [set()] * len(actions)
        for i in range(len(actions)):
            oneAction, oneSuccessors = actions[i], actionSuccessors[i]
            for j in range(i+1, len(actions)):
                twoAction, twoSuccessors = actions[j], actionSuccessors[j]
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

    
    def __ArgumentPair(ssp:MM_MDP, V:list, state:MM_MDP.State, oneAction, oneSuccessors, twoAction, twoSuccessors):
        oneAttacked, twoAttacked = set(), set()

        # Critical Question 2: Check for Defence (compare actions)
        oneExpectation = ssp.ActionExpectation(state, V, successors=oneSuccessors)
        twoExpectation = ssp.ActionExpectation(state, V, successors=twoSuccessors)
        result, tClass = ssp.CompareExpectations(oneExpectation, twoExpectation)

        # 0 indicates the argument is NOT vulnerable to attack; 1 means it is!
        oneActVul, twoActVul = Retrospection.vulnerable(result)

        # Critical Question 1: Check for inequality (compare arguments/successors)
        for oneIdx, oneSuccessor in enumerate(oneSuccessors):
            for twoIdx, twoSuccessor in enumerate(twoSuccessors):
                oneE = ssp.SuccessorExpectation(V, state, oneAction, oneSuccessor)
                twoE = ssp.SuccessorExpectation(V, state, twoAction, twoSuccessor)
                cq1, t = ssp.CompareExpectations(oneE, twoE, maxClass=tClass)

                # Track Attacker and Defender Non Acceptability
                if cq1==AttackResult.ATTACK and twoActVul:
                    twoAttacked.add(twoSuccessor)
                elif cq1==AttackResult.REVERSE and oneActVul:
                    oneAttacked.add(oneSuccessor)
        
            
        # When 'trap theory or above' does have influence, trap not in effect. Return normal
        # Or when not in a trap ,return normal:
        return oneAttacked, twoAttacked


    def vulnerable(result):
        vOne, vTwo = True, True # True means vulnerable; False means cannot be attacked (defended)
        if result==AttackResult.ATTACK:
            vOne = False # Attack arguments cannot be attacked
        elif result==AttackResult.REVERSE:
            vTwo = False # Defender arguments cannot be attacked
        elif result==AttackResult.ABSOLUTE_ATTACK:
            return False, True # Automatic attack on all defender arguments
        elif result==AttackResult.ABSOLUTE_REVERSE:
            return True, False # Automatic attack on all attacker arguments
        return vOne, vTwo


    def __ArgumentPathPair(ssp:MM_MDP, onePaths, twoPaths):
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


