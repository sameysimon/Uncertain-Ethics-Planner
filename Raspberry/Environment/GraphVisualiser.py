
import pygraphviz


def VisualiseExplicitGraph(mdp,solution,fileName='file'):
    stateNodes = range(len(mdp.states))
    stateActions = [mdp.getActions(mdp.states[s]) for s in stateNodes]

    stateLabels=[]
    for s in stateNodes:
        l=mdp.stateString(mdp.states[s]) + "\n"
        uStr, aStr = "", ""
        if 'utility' in solution.V.keys():
            uStr="v({utilValue})\n".format(
            utilValue=solution.V['utility'][s]
            )
        if 'absolute' in solution.V.keys():
            aStr="v({utilValue})\n".format(
            utilValue=solution.V['absolute'][s]
            )
        l = l + uStr + aStr
        stateLabels.append(l)

    stateActionLabels = {}
    for s in stateNodes:
        for a in stateActions[s]:
            actionTag, doneTag = "", ""
            successors = mdp.getActionSuccessors(mdp.states[s], a, readOnly=True)
            actionTag = t.EstimateString(t.Gather(successors, solution.V[t.tag]))
            for C in mdp.TheoryClasses:
                for t in C:

                    actionTag += t.tag + ": " + t.EstimateString(t.Gather())
            
            if s in solution.pi.keys():
                doneTag=""
                if solution.pi[s]==a:
                    doneTag="*"
            stateActionLabels["a{action}s{state}".format(action=a, state=s)] = actionTag + doneTag
            
            stateActionLabels["a{action}s{state}".format(action=a, state=s)] = a+doneTag
            doneTag=""

    actionSuccessors = []
    for s in stateNodes:
        sDict = {}
        actionSuccessors.append(sDict)
        for a in stateActions[s]:
            # Create Successor dictionary {action: [successor IDs]}
            successors = []
            for child in mdp.getActionSuccessors(mdp.states[s], a, readOnly=True):
                successors.append((child.targetState.id, child.probability))
            sDict[a]=successors

            # Create Action String tag
            doneTag = ""
            actionTag = t.EstimateString(t.Gather(successors, solution.V[t.tag]))
            stateActionLabels["a{action}s{state}".format(action=a, state=s)] = actionTag + doneTag

    VisualiseGraph(stateNodes, stateActions, stateLabels, stateActionLabels, actionSuccessors, fileName)




def VisualiseGraph(stateNodes,stateActions,stateLabels,stateActionLabels,actionSuccessors,fileName='file', showEmptyActions=False):
    print()
    G = pygraphviz.AGraph(directed=True)
    G.layout()
    # Draw nodes/states
    for s in stateNodes:
        G.add_node(s, shape='box', color='red', label=stateLabels[s])
    # Draw actions and arrows
    for s in stateNodes:
        for action in stateActions[s]:
            if len(actionSuccessors[s][action])==0 and showEmptyActions == False:
                continue # Don't bother render actions with no successors.
            stateActionID = "a{a}s{s}".format(a=action,s=s)
            G.add_node(stateActionID, shape='trapezium', color='blue', label=stateActionLabels[stateActionID]) # Add Action
            G.add_edge(s, stateActionID) #Arrow from parent state to action.

            for s_,p in actionSuccessors[s][action]:
                G.add_edge(stateActionID, s_, label=p)# Arrow from action to successor.
    G.draw("{fn}.pdf".format(fn=fileName),format='pdf',prog="dot")
    p = G.draw(format='svg',prog="dot")
    print(p)