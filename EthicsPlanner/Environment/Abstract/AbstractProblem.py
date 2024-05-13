import EthicsPlanner.Environment.GraphVisualiser as v
from EthicsPlanner.Environment.MultiMoralMDP import MM_MDP
from EthicsPlanner.Environment.Abstract.Utilitarian import Utilitarian
from EthicsPlanner.Environment.Abstract.Absolute import Absolute
import copy


class AbstractProblem(MM_MDP):

    def __init__(self, setup, theories=[['utility']]) -> None:
        MM_MDP.__init__(self)
        self.world = {}
        if setup:
            self.world = setup
        else:
            self.world = AbstractProblem.defaultSetup()
        self.stateFactory({'tile':0, 'utility':self.world['utilities'][0], 'forbidden':False}) # Create at least one initial state
        self.rules = [AbstractProblem.GraphMove, AbstractProblem.UtilityResult] # Add a transition rule
        self.Theories = [Utilitarian(), Absolute()]
        self.TheoryClasses = theories # Set the ethical theories

    def getActions(self, state:MM_MDP.State) -> list:
        return self.world['actions'][str(state.props['tile'])]

    # ****
    # Transition Rules
    # ****

    def GraphMove(self, props, prob, action):
        outcomes = []
        for dest, p in self.world['stateSpace'][props['tile']][action]:
            props_ = copy.deepcopy(props)
            prob_ = prob
            
            props_['tile'] = dest
            props_['utility'] = self.world['utilities'][props_['tile']]
            props_['forbidden'] = props_['tile'] in self.world['forbidden']
            prob_ *= p
            outcomes.append((props_, prob_))
        return outcomes
    
    def UtilityResult(self, props, prob, action):
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
        d['forbidden'] = []

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
    
    def stateString(self, state) -> str:
        return "t={tile}".format(week=state.props['tile'])
        


    def VisualiseCompleteGraph(mdp,fileName='file'):
        stateNodes = range(len(mdp.world['stateSpace']))
        stateActions = [mdp.world['stateSpace'][s].keys() for s in stateNodes]

        stateLabels = ["idx={idx}\nu={utility}\nf={forbid}".format(idx=s, utility=mdp.world['utilities'][s], forbid=s in mdp.world['forbidden']) for s in stateNodes]

        stateActionLabels = {}
        for s in stateNodes:
            for a in stateActions[s]:
                stateActionLabels["a{action}s{state}".format(action=a, state=s)] = a

        actionSuccessors = mdp.world['stateSpace']

        v.VisualiseGraph(stateNodes, stateActions, stateLabels, stateActionLabels, actionSuccessors, fileName)

    def VisualiseExplicitGraph(mdp,solution,fileName='file'):
        stateNodes = range(len(mdp.states))
        stateActions = [mdp.getActions(mdp.states[s]) for s in stateNodes]

        stateLabels=[]
        for s in stateNodes:
            l="t{tile}\n".format(tile=mdp.states[s].props['tile'])
            uStr, aStr = "", ""
            if 'utility' in solution.V.keys():
                uStr="u={utility}+v({utilValue})\n".format(
                utility=mdp.states[s].props['utility'],
                utilValue=solution.V['utility'][s]
                )
            if 'absolute' in solution.V.keys():
                aStr="d={utility}+v({utilValue})\n".format(
                utility=mdp.states[s].props['forbidden'],
                utilValue=solution.V['absolute'][s]
                )
            l = l + uStr + aStr
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
                for child in mdp.getActionSuccessors(mdp.states[s], a, readOnly=True):
                    successors.append((child.targetState.id, child.probability))
                sDict[a]=successors

        v.VisualiseGraph(stateNodes, stateActions, stateLabels, stateActionLabels, actionSuccessors, fileName)