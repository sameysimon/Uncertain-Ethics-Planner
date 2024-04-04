import copy
import pygraphviz

class AbstractBase(object):

    def __init__(self, setup) -> None:
        super(AbstractBase, self).__init__()
        self.world = {}
        if setup:
            self.world = setup
        else:
            self.world = AbstractBase.defaultSetup()
        self.stateFactory({'tile':0, 'utility':self.world['utilities'][0]}) # Create at least one initial state
        self.rules = [AbstractBase.GraphMove, AbstractBase.UtilityResult] # Add a transition rule


    # ****
    # Transition Rules
    # ****

    def GraphMove(self, transition, action):
        props, prob = transition
        outcomes = []
        
        for dest, p in self.world['stateSpace'][props['tile']][action]:
            props_ = copy.deepcopy(props)
            prob_ = prob
            
            props_['tile'] = dest
            props_['utility'] = self.world['utilities'][props_['tile']]
            prob_ *= p
            outcomes.append((props_, prob_))

        return outcomes
    
    def UtilityResult(self, transition, action):
        props, prob = transition
        #props_ = copy.deepcopy(props)
        #props_['utility'] = self.world['utilities'][props_['tile']]
        props['utility'] = self.world['utilities'][props['tile']]
        return [(props, prob)]


    # ****
    # Default Setup Function
    # ****
    def defaultSetup():
        d={}
        d['cost']=-1
        d['actions'] = {1:['A','B'], 2:['A', 'B'], 3:['A','B'], 4:['A', 'B']}
        d['utilities'] = [0,1,2,3,4]
        d['goalTiles'] = [4]

        # Initialise state space successor dicts
        d['stateSpace'] = [{},{},{},{}]
        
        # List of successor (tile,probability) for each state-action
        d['stateSpace'][1]['A'] = [(2,1)]
        d['stateSpace'][1]['B'] = [(2,1)]

        d['stateSpace'][2]['A'] = [(3,1)]
        d['stateSpace'][2]['B'] = [(3,1)]
        
        d['stateSpace'][3]['A'] = [(4,1)]
        d['stateSpace'][3]['B'] = [(4,1)]

        d['stateSpace'][4]['A'] = [(4,1)]
        d['stateSpace'][4]['B'] = [(4,1)]

        return d
    
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
        p = G.draw(format='svg',prog="dot")
        print(p)
                    
    