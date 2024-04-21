from Raspberry.Environment.MultiMoralMDP import MM_MDP
from Raspberry.Environment.Result import AttackResult
from Raspberry.Planner.Solution import BestSubGraph
import numpy as np
import pandas as pd

# Currently, only works on Multi-Moral MM_MDPs.
class Retrospection:
    
    class Attack:
        def __init__(self, source, target):
            self.sourceSuccessor=source
            self.targetSuccessor=target
    
    def RetrospectPaths(ssp:MM_MDP,policyPaths:list):
        pass

    def Retrospect(ssp:MM_MDP, state:MM_MDP.State, actions:list, actionSuccessors:list, V):
        actionAttacks = [[] for _ in actions]
        for i in range(len(actions)):
            oneAction, oneSuccessors = actions[i], actionSuccessors[i]
            for j in range(i+1, len(actions)):
                twoAction, twoSuccessors = actions[j], actionSuccessors[j]
                oneAttacked, twoAttacked = Retrospection.__ArgumentPair(ssp,V,state,oneAction,oneSuccessors,twoAction,twoSuccessors)
                actionAttacks[i].extend(oneAttacked)
                actionAttacks[j].extend(twoAttacked)        
        
        nonAcceptability = [0 for _ in actions]
        for idx, attacks in enumerate(actionAttacks):
            # Finds cumulative probability of attacked successors for action
            attackedSuccessors = set([a.targetSuccessor for a in attacks])
            na = Retrospection.GetProbability(attackedSuccessors)
            nonAcceptability[idx] = na
        
        Retrospection.RetrospectionTable(ssp, state, actions, actionSuccessors,actionAttacks,nonAcceptability, V)
        return nonAcceptability
    
    def GetProbability(successors):
        p = 0
        for s in successors:            
            p+=s.probability
        return p
   
    def __ArgumentPair(ssp:MM_MDP, V:list, state:MM_MDP.State, oneAction, oneSuccessors, twoAction, twoSuccessors):
        oneAttacks, twoAttacks = [],[]

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
                    a = Retrospection.Attack(source=oneSuccessor, target=twoSuccessor)
                    twoAttacks.append(a)
                elif cq1==AttackResult.REVERSE and oneActVul:
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



    def RetrospectionTable(ssp, state, actions, actionSuccessors, attackedArgs, nonAcceptability, V):
        # Generate columns
        bestaIdx = np.argmin(nonAcceptability)

        cols = []
        def makeColumn(aIdx, action, successor):
            nonlocal cols, bestaIdx
            if aIdx==bestaIdx:
                cols.append([action+"*", successor.targetState.id])
            else:
                cols.append([action, successor.targetState.id])

        Retrospection.__runOnActionSuccessor(actions, actionSuccessors, makeColumn)
        colsDF = pd.DataFrame(cols, columns=["",""])
        columns = pd.MultiIndex.from_frame(colsDF)

        
        index = []
        rows = []

        row = []   
        rows.append(row)
        index.append('Probability')
        def addProbability(aIdx, action, successor):
            nonlocal row
            row.append(str(successor.probability))
        Retrospection.__runOnActionSuccessor(actions, actionSuccessors, addProbability)

        for C in ssp.TheoryClasses:
            for t in C:
                index.append(t.tag)
                row = []
                rows.append(row)
                def addToRow(aIdx, action, successor):
                    nonlocal row, V
                    row.append(str(t.JudgeTransition(successor)) + "+" + str(V[t.tag][successor.targetState.id]))
                Retrospection.__runOnActionSuccessor(actions, actionSuccessors, addToRow)

        row = []   
        rows.append(row)
        index.append('Attacked by')
        def addAttacks(aIdx, action, successor):
            nonlocal row, attackedArgs
            attackSig = ""
            for a in attackedArgs[aIdx]:
                if a.targetSuccessor == successor:
                    attackSig+=str(a.sourceSuccessor.targetState.id) + " (" + a.sourceSuccessor.action + ")"
            row.append(attackSig)
        Retrospection.__runOnActionSuccessor(actions, actionSuccessors, addAttacks)
        
        
        row = []
        rows.append(row)
        index.append('Non-Acceptability')
        def addNonAccept(aIdx, action, successor):
            nonlocal nonAcceptability
            row.append(nonAcceptability[aIdx])
        Retrospection.__runOnActionSuccessor(actions, actionSuccessors, addNonAccept)
        

        df = pd.DataFrame(rows, columns=columns,index=index)

        Retrospection.saveToFile(state.props, df.to_html())


    def saveToFile(props, t):
        with open('template.html', 'r') as file:
            original = file.read()

        tagTable = "<div class='props'>"
        insert = original.find(tagTable)
        insert+=len(tagTable)
        modified = original[:insert] + str(props) + original[insert:]

        tagTable = "<div class='rTable'>"
        insert = modified.find(tagTable)
        insert+=len(tagTable)
        modified = modified[:insert] + t + modified[insert:]

        # Write
        with open('output.html', 'w') as file:
            file.write(modified)



    def __runOnActionSuccessor(actions, actionSuccessors, fn):
        for aIdx in range(len(actions)):
            action = actions[aIdx]
            for s in actionSuccessors[aIdx]:
                fn(aIdx, action, s)