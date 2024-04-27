from datetime import datetime
import numpy as np
import pandas as pd
class Logger:
    history = []
    silent = False
    debug=False
    def add(new):
        if Logger.silent:
            return
        Logger.history.append(new)
    
    def ToString():
        s = ""
        for l in Logger.history:
            s += l
        return s

    def clear():
        Logger.history = []

    def FlushToFile():
        f = open('TrapTest.txt', 'a')
        f.write(Logger.ToString())
        f.close()
        Logger.clear()

    # Retrospection Table!
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

        Logger.__runOnActionSuccessor(actions, actionSuccessors, makeColumn)
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
        Logger.__runOnActionSuccessor(actions, actionSuccessors, addProbability)

        for C in ssp.TheoryClasses:
            for t in C:
                # Add the equation
                index.append(t.tag)
                row = []
                rows.append(row)
                for aIdx in range((len(actions))):
                    r = t.GatherString(actionSuccessors[aIdx], V[t.tag])
                    row.extend(r)

                # Add the 'summed' action result
                row = []
                rows.append(row)
                index.append(t.tag + "=")
                def addToRow(aIdx, action, successor):
                    nonlocal row, V
                    row.append(t.EstimateString(t.Gather(actionSuccessors[aIdx], V[t.tag])))
                Logger.__runOnActionSuccessor(actions, actionSuccessors, addToRow)
                

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
        Logger.__runOnActionSuccessor(actions, actionSuccessors, addAttacks)
        
        
        row = []
        rows.append(row)
        index.append('Non-Acceptability')
        def addNonAccept(aIdx, action, successor):
            nonlocal nonAcceptability
            row.append(nonAcceptability[aIdx])
        Logger.__runOnActionSuccessor(actions, actionSuccessors, addNonAccept)
        

        df = pd.DataFrame(rows, columns=columns,index=index)

        Logger.saveToFile(state, actions, actionSuccessors, df.to_html())
        i = input('Retrospection Table Built. Enter To Continue; Q to exit Debug mode.')
        Logger.debug = i!='Q'
            

    def saveToFile(state, actions, actionSuccessors, t):
        with open('template.html', 'r') as file:
            original = file.read()

        tagTable = "<div class='props'>"
        insert = original.find(tagTable)
        insert+=len(tagTable)
        modified = original[:insert] + str(state.props) + original[insert:]

        tagTable = "<div class='rTable'>"
        insert = modified.find(tagTable)
        insert+=len(tagTable)
        modified = modified[:insert] + t + modified[insert:]

        tagTable = "<div class='sProps'>"
        insert = modified.find(tagTable)
        insert+=len(tagTable)
        for aIdx in range(len(actions)):
            p ="<h4>Action: {action}</h4>".format(action=actions[aIdx])
            for s in actionSuccessors[aIdx]:
                p+="<h5>Successor Target ID: {id}</h5>{prop}".format(id=s.targetState.id, prop=str(s.targetState.props))
            modified = modified[:insert] + p + modified[insert:]


        # Write
        with open('output.html', 'w') as file:
            file.write(modified)

    def __runOnActionSuccessor(actions, actionSuccessors, fn):
        for aIdx in range(len(actions)):
            action = actions[aIdx]
            for s in actionSuccessors[aIdx]:
                fn(aIdx, action, s)