from tabulate import tabulate

class Log:
    messages=[]
    cycle=0
    active=False
    def retrospection(state, actions, nonaccept, bestAction):
        if Log.active==False:
            return
        m="For state {s}, there are {l} ethical actions:\n".format(l=len(actions), s=state.id)
        for idx, a in enumerate(actions):
            m+= "   Action {a} with {n} non-acceptability".format(a=a,n=nonaccept[idx])
            if a==bestAction:
                m+= "*"
            m+="\n"
        m+= "Selected action {a}".format(a=bestAction)
        Log.__addToLog(m)
    
    def EstimateMatrix(E, showStates=[]):
        if Log.active==False:
            return
        m="\After Cycle {c}, Updated values in Estimate Matrix:\n".format(c=Log.cycle)
        table = {}
        for key in E:
            table[key] = [E[key][index] for index in showStates]

        m += tabulate(table,headers="keys", tablefmt="grid", showindex=True)
        Log.__addToLog(m)
        
    def NegativeHR(state, action, attackingAction, attacks):
        if Log.active==False:
            return
        m = "Negative retrospection for action {a} on state {s}.\n".format(state.id,action)
        m+= "Should take {aa} because: \n".format(attackingAction)
        for sourceSuccessor, targetSuccessor in attacks:
            m+= "   If we reach: {targetID} with probability {p}, \n".format(targetID=targetSuccessor.targetState.id, p=targetSuccessor.probability)
            m+= "   Then we miss: {sourceID} with probability {p} \n".format(sourceID=sourceSuccessor.targetState.id, p=sourceSuccessor.probability)
        Log.__addToLog(m)

    def VisualiseGraph(bpsg, ssp):
        if Log.active==False:
            return
        ssp.VisualiseExplicitGraph(bpsg, fileName='temp/update'+str(Log.cycle))

    def newCycle():
        if Log.active==False:
            return
        Log.cycle+=1

    def __addToLog(m):
        if Log.active==False:
            return
        Log.messages.append(m+"\n")

    def Flush():
        if Log.active==False:
            return
        file = open('temp/data'+str(Log.cycle)+'.txt','w')
        for m in Log.messages:
            file.write(m)
        file.close()
        Log.messages=[]

