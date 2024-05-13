from EthicsPlanner.Environment.GeneralMDP import MDP
from EthicsPlanner.Environment.Theory.Utilitarianism import Utilitarianism

class EducationUtility(Utilitarianism):

    gradeMap = {'A':5,'B':3,'C':1,'D':-1,'E':-2,'F':-3}

    def JudgeTransition(self, successor:MDP.Successor):
        oldProps = successor.sourceState.props
        props = successor.targetState.props
        avgGrade = 0
        for i in range(props['totalStudents']):
            avgGrade+=(props['grades'][i] - oldProps['grades'][i])

        return avgGrade
    
    def StateHeuristic(self, state:MDP.State):
        # No possible Grade ups if 0 sessions
        totalWeeks = state.props['totalWeeks'] - state.props['week']
        studentsThisWeek = (state.props['totalStudents']- state.props['student'])
        totalSessions = (totalWeeks*state.props['totalStudents']) + studentsThisWeek
        if totalSessions==0:
            return 0
        
        # Heuristic is max number of average possible grade ups per student.
        
        gradeUps = 0
        for i in range(0, state.props['totalStudents']):
            sessions = totalWeeks+1 if i>= state.props['student'] else totalWeeks
            distToMax = state.props['maxGrade'] - state.props['grades'][i]
            gradeUps += min(sessions, distToMax)*0.4
            #gradeUps += state.props['standardChances'][i]
        
        # Looking for the average number of grade ups across students.
        h = gradeUps
        return h
