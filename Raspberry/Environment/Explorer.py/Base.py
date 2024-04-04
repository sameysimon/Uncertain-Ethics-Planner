import copy

class ExplorerBase(object):

    def __init__(self, setup) -> None:
        super(ExplorerBase, self).__init__()
        self.stateFactory({'time':0, 'people_saved':0, 'camp_time':0, 'comm_time':0, 'position':'start', 'operating':False}) # Create at least one initial state
        self.rules = [ExplorerBase.Time, ExplorerBase.ExploreEffects, ExplorerBase.Decide] # Add a transition rule

    # ****
    # Transition Rules
    # ****

    def ExploreEffects(self, transition, action):
        props, prob = transition
        if props[0]['position']!= 'exploring':
            return [transition]
        outcomes=[]
        time = props['time']
        if action=='risk': # More chance of finding someone; chance of termination.
            # Bad outcome.
            props_ = copy.deepcopy(props)
            props_['operating']==False
            p1 = round(0.15*time,2) # More likely with time.
            outcomes.append(props_, prob*p1)
            
            # Good outcome.
            props_ = copy.deepcopy(props)
            props_['people_saved']+=1
            p2 = round(0.5/time,2) # less likely with time.
            outcomes.append(props_, prob*p2)
            if 1-p2-p1>=0:
                # Medium outcome (only time passes)
                props_ = copy.deepcopy(props)
                outcomes.append(props_, prob*1-p2-p1)
        elif action=='safe': # Less chance of finding someone; no chance of termination.
            # Find someone 
            props_ = copy.deepcopy(props)
            props_['people_saved']+=1
            p = round(0.25/time,2) # less likely with time.
            outcomes.append(props_, prob*p)
            # Nothing happens
            props_ = copy.deepcopy(props)
            outcomes.append(props_, prob*1-p)

        return outcomes

    def NonExploreEffects(self, transition, action):
        props, prob = transition
        if props['position']=='camp':
            props['camp_time']+=1
        if props['position']=='comms':
            props['comm_time']+=1
        return [props, prob]

    def Decide(self, transition, action):
        props, prob = transition
        if props['position']=='start':
            if action=='explore':
                props['position']='exploring'

            elif action=='camp':
                props['position']='camp'

            elif action=='comms':
                props['position']='comms'
        elif props['operating']:
            if action=='return':
                props['position']='start'

        return [(props, prob)]

    


    
    def Time(self, transition, action):
        props, prob = transition
        props['time']+=1
        return [props, prob]



 
    # ****
    # Visualisation Functions
    # ****
    def VisualiseExplicitGraph(self,solution,fileName='file'):
        stateNodes = range(len(self.states))
        stateActions = [self.getActions(self.states[s]) for s in stateNodes]

        stateLabels=[]
        for s in stateNodes:
            l="t={tile}\nu={utility}+v({utilValue})".format(
                tile=self.states[s].props['tile'], 
                utility=self.states[s].props['utility'],
                utilValue=solution.V['utility'][s]
                )
            stateLabels.append(l)        

        stateActionLabels = {}
        for s in stateNodes:
            for a in stateActions[s]:
                if s in solution.pi.keys():
                    doneTag=""
                    if solution.pi[s]==a:
                        doneTag="\nCHOSEN"
                stateActionLabels["a{action}s{state}".format(action=a, state=s)] = a+doneTag
                doneTag=""

        actionSuccessors = []
        for s in stateNodes:
            sDict = {}
            actionSuccessors.append(sDict)
            for a in stateActions[s]:
                successors = []
                for child in self.getActionSuccessors(self.states[s], a, readOnly=True):
                    successors.append((child.targetState.id, child.probability))
                sDict[a]=successors

        self.VisualiseGraph(stateNodes, stateActions, stateLabels, stateActionLabels, actionSuccessors, fileName)

    def VisualiseCompleteGraph(self,fileName='file'):
        stateNodes = range(len(self.world['stateSpace']))
        stateActions = [self.world['stateSpace'][s].keys() for s in stateNodes]

        stateLabels = ["idx={idx}\nu={utility}".format(idx=s, utility=self.world['utilities'][s]) for s in stateNodes]

        
        stateActionLabels = {}
        for s in stateNodes:
            for a in stateActions[s]:
                stateActionLabels["a{action}s{state}".format(action=a, state=s)] = a

        actionSuccessors = self.world['stateSpace']

        self.VisualiseGraph(stateNodes, stateActions, stateLabels, stateActionLabels, actionSuccessors, fileName)

    def VisualiseGraph(self,stateNodes,stateActions,stateLabels,stateActionLabels,actionSuccessors,fileName='file', showEmptyActions=False):
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
                    
    