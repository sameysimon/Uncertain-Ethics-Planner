from Raspberry.Environment.MultiMoralMDP import MM_MDP
from Raspberry.Environment.TeacherBot.Utilitarian import EducationUtility
import Raspberry.Environment.GraphVisualiser as v
from copy import deepcopy
from enum import Enum

class TeacherProblem(MM_MDP):

    def __init__(self, initialProps=None, theoryClasses=[[EducationUtility()]]) -> None:
        super().__init__()
        if initialProps==None:
            initialProps=TeacherProblem.defaultProps
        self.stateFactory(initialProps) # Create at least one initial state
        self.rules = [TeacherProblem.Standard, TeacherProblem.PosCompare, TeacherProblem.NegCompare, TeacherProblem.NextSession] # Add a transition rule
        self.TheoryClasses=theoryClasses
    defaultProps = {
            'week':1,
            'student':0,
            'grades':[4, 3],
            'maxGrade':10,
            'maxStress':5,
            'stress':[2,2], # Stress level: 5 is maximum.
            'totalStudents':2,
            'totalWeeks':2,
            'standardChances': [0.1,0.1]
        }

    

    def __isStudentLowest(self, props):
        g = props['grades'][props['student']]
        return min(props['grades'])==g

    def __changeStress(prop, delta, studentIdx):
        p = prop['stress'][studentIdx] + delta
        if p<0:
            p=0
        if p>5:
            p=5
        prop['stress'][studentIdx] = p
    
    def __changeGrade(prop, delta, studentIdx):
        g = prop['grades'][studentIdx] + delta
        if g<0:
            g=0
        if g>prop['maxGrade']:
            g=5
        prop['grades'][studentIdx] = g
    
        
    def getActions(self, state):
        # Reached the end
        if state.props['week'] > state.props['totalWeeks']:
            return []
        # Not at the end
        if self.__isStudentLowest(state.props):
            # If current student is lowest score, must lie to positively compare -> pos_lie
            #   can honestly negatively compare -> neg_hon
            return ['standard', 'pos_lie', 'neg_hon']
        else:
            # If current student is not lowest scored, can honestly positively compare -> pos_hon
            #   must lie to negatively compare -> neg_lie
            return ['standard', 'pos_hon', 'neg_lie']


    # standard action
    def Standard(self, props, prob, action):
        if action!='standard':
            return [(props, prob)]
        # Standard action, +0.1 chance of grade increase at the end.
        o = []
        if props['week']!=props['totalWeeks']:
            # Standard increase in chance of grade_up
            props_ = deepcopy(props)
            props_['standardChances'][props_['student']]*=1.05
            o.append((props_, prob))
            return o
        
        # In last week, chance of natural grade increase.

        # Chance of increase
        props_, prob_ = deepcopy((props, prob))
        props_['grades'][props_['student']] += 1
        prob_ *= props_['standardChances'][props_['student']]
        o.append((props_, prob_))

        # Chance of no increase
        props_, prob_ = deepcopy((props, prob))
        prob_ *= (1 - props_['standardChances'][props_['student']])
        o.append((props_, prob_))

        return o
    
    # pos_lie and pos_hon actions
    def PosCompare(self, props, prob, action):
        if action!='pos_lie' and action!='pos_hon':
            return [(props, prob)]

        o = []
        # Chance of decreasing stress by 1 only.
        props_ = deepcopy(props)
        TeacherProblem.__changeStress(props_, -1, props_['student'])
        o.append((props_, prob))
        return o

    # neg_lie and neg_hon actions
    def NegCompare(self, props, prob, action):
        if action!='neg_lie' and action!='neg_hon':
            return [(props, prob)]
        
        o = []
        # OUTCOME 1: 40% CHANCE
        props_, prob_ = deepcopy((props, prob))
        # Boost grade by 1
        TeacherProblem.__changeGrade(props_, 1, props_['student'])
        # Boost chance of ending garde increase.
        fracWeeksRemaining = (props_['totalWeeks']-props_['week']) / props_['totalWeeks']
        props_['standardChances'][props_['student']]*= (1 + fracWeeksRemaining)*4
        prob_*=0.4
        o.append((props_, prob_))


        # OUTCOME 2: 60% CHANCE
        # Boost grade by 1
        props_, prob_ = deepcopy((props, prob))
        prob_*=0.6
        o.append((props_, prob_))
        return o


    # Saying the student is worse than another.
    # Chance of increasing stress level.
    # Will improve grade.
    def badCompare(self, props, prob):
        o = []
        # 1/2 chance of increasing stress and grade by 1 only.
        props_, prob_ = deepcopy((props, prob))
        props_['mental'][props_['student']]+=1
        props_['grades'][props_['student']] += 1
        prob_ *= 0.5
        o.append((props_, prob_))

        # 1/2 chance of increasing grade by 1 only.
        props_, prob_ = deepcopy((props, prob))
        props_['grades'][props_['student']] += 1
        prob_ *= 0.5
        o.append((props_, prob_))

        return o

        
    def NextSession(self, props, prob, action):
        # After each action, advance to next student.
        # After each student, advance to next week.
        props=deepcopy(props)
        if props['student']==props['totalStudents']-1:
            props['week']+=1
            props['student']=0
        else:
            props['student']+=1

        return [(props, prob)]


    def stateString(self, state) -> str:
        p = state.props
        s="ID={id} week={week}\n".format(week=p['week'], id=state.id)
        for idx in range(0, state.props['totalStudents']):
            if state.props['student']==idx:
                s+="*"
            s+="Student {i}: (grd:{grade}+{finChance},  str:{stress})\n".format(
                i=idx, 
                finChance=round(p['standardChances'][idx],2),
                grade=p['grades'][idx], 
                stress=p['stress'][idx])
        return s
