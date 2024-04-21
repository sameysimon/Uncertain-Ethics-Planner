from Raspberry.Environment.GeneralMDP import MDP
from Raspberry.Environment.Theory.Utilitarianism import Utilitarianism

class EducationUtility(Utilitarianism):

    gradeMap = {'A':5,'B':3,'C':1,'D':-1,'E':-2,'F':-3}

    def JudgeTransition(self, successor:MDP.Successor):
        props = successor.targetState.props
        avgGrade = 0
        for i in range(props['totalStudents']):
            avgGrade+=props['grades'][i]
        avgGrade /= props['totalStudents']-1

        return avgGrade
    
    def StateHeuristic(self, state:MDP.State):
        #  max grade * (students remaining this week + (total students * weeks remaining))
        gradesRemaining = state.props['totalStudents'] - state.props['student']
        gradesRemaining += (state.props['totalStudents']) * (state.props['totalWeeks'] - state.props['week'] - 1)
        gradesRemaining *= 5
        return gradesRemaining