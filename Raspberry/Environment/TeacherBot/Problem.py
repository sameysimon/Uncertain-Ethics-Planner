from Raspberry.Environment.MultiMoralMDP import MM_MDP

from Raspberry.Environment.TeacherBot.Utilitarian import EducationUtility
import Raspberry.Environment.GraphVisualiser as v
from copy import deepcopy

class TeacherBotBase:
    def __init__(self,setup=None) -> None:
        if setup==None:
            setup=self.default()
        self.stateFactory(setup) # Create at least one initial state
        self.rules = [TeacherBotBase.Standard, TeacherBotBase.PosCompare, TeacherBotBase.NegCompare, TeacherBotBase.NextSession] # Add a transition rule

    def default(self):
        return {
            'week':1,
            'student':0,
            'grades':[4, 3],
            'stress':[2,2], # Stress level: 5 is maximum.
            'totalStudents':2,
            'totalWeeks':3,
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
        if g>5:
            g=5
        prop['grades'][studentIdx] = g
        
    def getActions(self, state):
        # Reached the end
        if state.props['week'] == state.props['totalWeeks']:
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
    def Standard(self, transition, action):
        # Standard action, +0.1 chance of grade increase at the end.
        props, prob = deepcopy(transition)
        o = []
        if props['week']!=props['totalWeeks']:
            # Standard increase in chance of grade_up
            props_, prob_ = deepcopy(transition)
            props_['standardChances'][props_['student']]+=0.1
            o.append((props_, prob_))
            return o
        
        # In last week, chance of natural grade increase.

        # Chance of increase
        props_, prob_ = deepcopy(transition)
        props_['grades'][props_['student']] += 1
        prob_ *= props_['standardChances'][props_['student']]
        o.append((props_, prob_))

        # Chance of no increase
        props_, prob_ = deepcopy(transition)
        prob_ *= (props_['standardChances'][props_['student']] - 1)
        o.append((props_, prob_))

        return o
    
    # pos_lie and pos_hon actions
    def PosCompare(self, transition, action):
        if action!='pos_lie' or action!='pos_hon':
            return [transition]

        o = []
        # Chance of decreasing stress by 1 only.
        props_, prob_ = deepcopy(transition)
        TeacherBotBase.__changeStress(props_, -1, props_['student'])
        o.append((props_, prob_))
        return o

    # neg_lie and neg_hon actions
    def NegCompare(self, transition, action):
        if action!='pos_lie' or action!='pos_hon':
            return [transition]
        
        o = []
        props_, prob_ = deepcopy(transition)
        TeacherBotBase.__changeGrade(props_, 1, props_['student'])
        TeacherBotBase.__changeStress(props_, -1, props_['student'])
        prob_*=0.25
        o.append((props_, prob_))

        props_, prob_ = deepcopy(transition)
        TeacherBotBase.__changeGrade(props_, 1, props_['student'])
        TeacherBotBase.__changeGrade(props_, -1, props_['student'])
        prob_*=0.25
        o.append((props_, prob_))


    # Saying the student is worse than another.
    # Chance of increasing stress level.
    # Will improve grade.
    def badCompare(self, transition):
        o = []
        # 1/2 chance of increasing stress and grade by 1 only.
        props_, prob_ = deepcopy(transition)
        props_['mental'][props_['student']]+=1
        props_['grades'][props_['student']] += 1
        prob_ *= 0.5
        o.append((props_, prob_))

        # 1/2 chance of increasing grade by 1 only.
        props_, prob_ = deepcopy(transition)
        props_['grades'][props_['student']] += 1
        prob_ *= 0.5
        o.append((props_, prob_))

        return o

        
    def NextSession(self, transition, action):
        # After each action, advance to next student.
        # After each student, advance to next week.
        props, prob = transition
        if props['student']==props['totalStudents']-1:
            props['week']+=1
            props['student']=0
        else:
            props['student']+=1

        return [(props, prob)]


    def stateString(self, state) -> str:
        p = state.props
        s="wk={week}".format(week=p['week'])
        for idx in range(0, state.props['totalStudents']):
            s+="{i}: g:{grade}.{finChance} m:{stress}\n".format(
                i=idx, 
                finChance=round(p['standardChances'][idx],2),
                grade=p['grades'][idx], 
                stress=p['stress'][idx])
        return s


class MultiTeacherBot(MM_MDP, TeacherBotBase):
    def __init__(self) -> None:
        MM_MDP.__init__(self)
        TeacherBotBase.__init__(self)
        self.TheoryClasses = [[EducationUtility()]]