from EthicsPlanner.Environment.MultiMoralMDP import MM_MDP
from EthicsPlanner.Environment.Result import AttackResult
from EthicsPlanner.Planner.Solution import BestSubGraph
from EthicsPlanner.Planner.Log import Logger
import numpy as np
import pandas as pd

# Currently, only works on Multi-Moral MM_MDPs.
class Retrospection:
    
    class Attack:
        def __init__(self, source, target):
            self.sourceSuccessor=source
            self.targetSuccessor=target


    def Retrospect(mdp:MM_MDP, state:MM_MDP.State, actions:list, actionSuccessors:list, V):
        actionAttacks = [[] for _ in actions]
        for i in range(len(actions)):
            oneAction, oneSuccessors = actions[i], actionSuccessors[i]
            for j in range(i+1, len(actions)):
                twoAction, twoSuccessors = actions[j], actionSuccessors[j]
                oneAttacked, twoAttacked = Retrospection.__ArgumentPair(mdp,V,state,oneAction,oneSuccessors,twoAction,twoSuccessors)
                actionAttacks[i].extend(oneAttacked)
                actionAttacks[j].extend(twoAttacked)        
        
        nonAcceptability = [0 for _ in actions]
        for idx, attacks in enumerate(actionAttacks):
            # Finds cumulative probability of attacked successors for action
            na = Retrospection.GetProbability(attacks)
            nonAcceptability[idx] = na

        if Logger.debug:
            Logger.RetrospectionTable(mdp, state, actions, actionSuccessors,actionAttacks,nonAcceptability, V)
        return nonAcceptability
    
    def GetProbability(attacks):
        p = 0
        for s in [a.targetSuccessor for a in attacks]:            
            p+=s.probability
        return p
   
    def __ArgumentPair(mdp:MM_MDP, V:list, state:MM_MDP.State, oneAction, oneSuccessors, twoAction, twoSuccessors):
        oneAttacks, twoAttacks = [],[]

        # Critical Question 2: Check for Defence (compare actions)
        oneExpectation = mdp.ActionExpectation(state, V, successors=oneSuccessors)
        twoExpectation = mdp.ActionExpectation(state, V, successors=twoSuccessors)
        result, tClass = mdp.CompareExpectations(oneExpectation, twoExpectation)

        # 0 indicates the argument is NOT vulnerable to attack; 1 means it is!
        oneActVul, twoActVul = Retrospection.vulnerable(result)

        # Critical Question 1: Check for inequality (compare arguments/successors)
        for oneIdx, oneSuccessor in enumerate(oneSuccessors):
            for twoIdx, twoSuccessor in enumerate(twoSuccessors):
                oneE = mdp.SuccessorExpectation(V, state, oneAction, oneSuccessor)
                twoE = mdp.SuccessorExpectation(V, state, twoAction, twoSuccessor)
                cq1, t = mdp.CompareExpectations(oneE, twoE, maxClass=tClass)

                # Track Attacker and Defender Non Acceptability
                if (cq1==AttackResult.ATTACK or cq1==AttackResult.DILEMMA) and twoActVul:
                    a = Retrospection.Attack(source=oneSuccessor, target=twoSuccessor)
                    twoAttacks.append(a)
                if (cq1==AttackResult.REVERSE or cq1==AttackResult.DILEMMA) and oneActVul:
                    a = Retrospection.Attack(source=twoSuccessor, target=oneSuccessor)
                    oneAttacks.append(a)
        
            
        # When 'trap theory or above' does have influence, trap not in effect. Return normal
        # Or when not in a trap ,return normal:
        return oneAttacks, twoAttacks


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


