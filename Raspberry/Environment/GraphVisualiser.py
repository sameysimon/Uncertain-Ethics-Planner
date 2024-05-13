
import pygraphviz


def VisualiseSolutionGraph(mdp, solution, fileName='SolutionGraph'):
    stateNodes = solution.states
    stateActions = {}
    for s in stateNodes:
        stateActions[s]=[solution.pi[s]] if s in solution.pi else []
    stateLabels={}
    for s in stateNodes:
        l=mdp.stateString(mdp.states[s]) + "\n"
        uStr, aStr = "", ""
        if 'utility' in solution.V.keys():
            uStr="V_u({utilValue}\n".format(
            utilValue=round(solution.V['utility'][s],3)
            )
        if 'absolute' in solution.V.keys():
            aStr="V_a={utilValue}\n".format(
            utilValue=solution.V['absolute'][s]
            )
        if 'wellbeing' in solution.V.keys():
            aStr="V_a={wValue}\n".format(
            wValue=solution.V['wellbeing'][s]
            )
        l = l + uStr + aStr
        stateLabels[s] = l

    stateActionLabels = {}
    for s in stateNodes:
        for a in stateActions[s]:
            actionTag= "{ac}\n".format(ac=a)
            successors = mdp.getActionSuccessors(mdp.states[s], a, readOnly=True)
            
            for t in mdp.Theories:
                actionTag += t.tag + ": " + t.EstimateString(t.Gather(successors, solution.V[t.tag])) + "\n"
            
            stateActionLabels["a{action}s{state}".format(action=a, state=s)] = actionTag

    actionSuccessors = {}
    for s in stateNodes:
        sDict = {}
        actionSuccessors[s] = sDict
        for a in stateActions[s]:
            # Create Successor dictionary {action: [successor IDs]}
            successors = []
            for child in mdp.getActionSuccessors(mdp.states[s], a, readOnly=True):
                successors.append((child.targetState.id, child.probability))
            sDict[a]=successors


    VisualiseGraph(stateNodes, stateActions, stateLabels, stateActionLabels, actionSuccessors, fileName)

def VisualiseExplicitGraph(mdp,solution,fileName='ExplicitGraph'):
    stateNodes = range(len(mdp.states))
    stateActions = [mdp.getActions(mdp.states[s]) for s in stateNodes]
    stateLabels=[]
    for s in stateNodes:
        l=mdp.stateString(mdp.states[s]) + "\n"
        uStr, aStr = "", ""
        if 'utility' in solution.V.keys():
            uStr="V_u({utilValue}\n".format(
            utilValue=round(solution.V['utility'][s],3)
            )
        if 'absolute' in solution.V.keys():
            aStr="V_a={utilValue}\n".format(
            utilValue=solution.V['absolute'][s]
            )
        l = l + uStr + aStr
        stateLabels.append(l)

    stateActionLabels = {}
    for s in stateNodes:
        for a in stateActions[s]:
            actionTag, doneTag = "{ac}\n".format(ac=a), ""
            successors = mdp.getActionSuccessors(mdp.states[s], a, readOnly=True)
            for C in mdp.TheoryClasses:
                for tag in C:
                    t = mdp.getTheoryByTag(tag)
                    actionTag += t.tag + ": " + t.EstimateString(t.Gather(successors, solution.V[t.tag])) + "\n"
            actionTag=actionTag[:-3]
            if s in solution.pi.keys():
                doneTag=""
                if solution.pi[s]==a:
                    doneTag="\nCHOSEN"
            stateActionLabels["a{action}s{state}".format(action=a, state=s)] = actionTag + doneTag
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