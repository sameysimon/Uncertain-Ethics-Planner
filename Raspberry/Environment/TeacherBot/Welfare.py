from Raspberry.Environment.GeneralMDP import MDP
from Raspberry.Environment.Theory.Utilitarianism import Utilitarianism

class Wellbeing(Utilitarianism):

    def __init__(self, discount=0.9) -> None:
        self.tag='wellbeing'
        self. discount=discount

    def JudgeTransition(self, successor:MDP.Successor):
        # Utility in decreasing stress.
        oldProps = successor.sourceState.props
        props = successor.targetState.props
        strDelta = 0
        for i in range(props['totalStudents']):
            strDelta+= (oldProps['stress'][i] - props['stress'][i])
        
        strDelta /= props['totalStudents']
        return strDelta
    
    def StateHeuristic(self, state:MDP.State):
        # No possible stress relief if 0 sessions
        totalWeeks = state.props['totalWeeks'] - state.props['week']
        studentsThisWeek = (state.props['totalStudents']- state.props['student'])
        totalSessions = (totalWeeks*state.props['totalStudents']) + studentsThisWeek
        if totalSessions==0:
            return 0
        
        # Heuristic is max number of stress decrements per student.
        util = 0
        for i in range(0, state.props['totalStudents']):
            sessions = totalWeeks+1 if i>= state.props['student'] else totalWeeks
            distToMax = state.props['maxStress'] - state.props['stress'][i]
            util += min(sessions, distToMax)*0.7
        
        # Looking for the average number of grade ups across students.
        h = util / (state.props['totalStudents'])
        return h
