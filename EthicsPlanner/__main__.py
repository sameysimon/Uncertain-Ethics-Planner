from EthicsPlanner.Planner.MDP_Solvers.MM_Heuristic import Solver as MM_LAO
from EthicsPlanner.Planner.MDP_Solvers.MM_ValueIteration import Multi_ValueIteration as MM_VI
from EthicsPlanner.Planner.MDP_Solvers.SM_Heuristic import Singleton_HeuristicSolver as SM_LAO
from EthicsPlanner.Planner.MDP_Solvers.SM_ValueIteration import Singleton_ValueIteration as SM_VI
from EthicsPlanner.Environment.TeacherBot.Problem import TeacherProblem
import EthicsPlanner.Environment.GraphVisualiser as v
from EthicsPlanner.Planner.Log import Logger
import os
import time
import sys
import EthicsPlanner.record_experiment as recorder
import pandas as pd
import argparse



if '-debug' in sys.argv:
    Logger.debug=True


# 1. CREATE PROBLEM
M = [
    [['utility', 'wellbeing']], 
    [['utility'], ['wellbeing']],
    [['wellbeing'], ['utility']],
    [['absolute'], ['utility', 'wellbeing']],
    [['utility', 'wellbeing'], ['absolute']],
    [['utility', 'wellbeing', 'absolute']]
    ]

singleTheories = ['utility', 'wellbeing', 'absolute']

def runExperiments():
    weeks = args.weeks

    if args.algo == 'SM_ILAO':
        tc = singleTheories[args.theories]
        mdp = TeacherProblem(theoryClasses=M[5],horizon=weeks)
        solver = SM_LAO()
        t1 = time.process_time()
        bpsg = solver.solve(mdp, theoryTag=tc)
        t2 = time.process_time()
        print('done')
        recorder.record_LAO(mdp, bpsg, solver, tc, t2-t1, weeks, 'SM_ILAO', filename=args.outputFiles)
        if args.graph:
            fn=os.cwd() + args.outputFiles+'_graph'
            v.VisualiseSolutionGraph(mdp, bpsg, fileName=fn)
            print('Graph visualised at ' + fn)
    elif args.algo == 'MM_VI':
        tc = M[args.theories]
        mdp = TeacherProblem(theoryClasses=tc,horizon=weeks)
        solver = MM_VI()
        t1 = time.process_time()
        pi = solver.solve(mdp)
        t2 = time.process_time()
        print('done')
        return recorder.record_VI(mdp, pi, solver, tc, t2-t1, weeks,'MM_VI', filename=args.outputFiles)
    elif args.algo == 'SM_VI':
        tc = singleTheories[args.theories]
        mdp = TeacherProblem(theoryClasses=M[5],horizon=weeks)
        solver = SM_VI()
        t1 = time.process_time()
        pi = solver.solve(mdp,theoryTag=tc)
        t2 = time.process_time()
        print('done')
        return recorder.record_VI(mdp, pi, solver, tc, t2-t1, weeks,'SM_VI', filename=args.outputFiles)
    elif args.algo == 'MM_ILAO':
        tc = M[args.theories]
        mdp = TeacherProblem(theoryClasses=tc,horizon=weeks)
        solver = MM_LAO()
        t1 = time.process_time()
        bpsg = solver.solve(mdp)
        t2 = time.process_time()
        print('done')
        recorder.record_LAO(mdp, bpsg, solver, tc, t2-t1, weeks, 'MM_ILAO', filename=args.outputFiles)
        if args.graph:
            fn=os.cwd() + args.outputFiles+'_graph'
            v.VisualiseSolutionGraph(mdp, bpsg, fileName=fn)
            print('Graph visualised at ' + fn)
    else:   
        print('No such algorithm.')



def output(name):    
    df = pd.read_csv(os.getcwd() + '/{fn}.csv'.format(fn=name))
    average_time_per_theory = df.groupby('Theories')['Time'].mean()
    print(average_time_per_theory.head())
    average_time_per_theory.to_csv(os.getcwd() + '/{fn}.csv'.format(fn=name+'_TIMES'))






parser = argparse.ArgumentParser()
helpStr=''
for i in range(len(M)):
    helpStr+= str(i) + '-' + str(M[i]) + ' ; '

# Select Theories
parser.add_argument('--theories', type=int, default=1, help='select moral theories by index: Singleton case:\n 0-utility\n 1-wellbeing\n 2-absolute\n \n Multi-Moral Case:\n' + helpStr)
# Set number of weeks
parser.add_argument('--weeks', type=int, default=5, help='number of weeks in the simulation.')
# Choose the algorithm
parser.add_argument('--algo', type=str, default='MM_ILAO', help='select algorithm: SM_ILAO, MM_ILAO, SM_VI, MM_VI')
# Choose the output name
parser.add_argument('--outputFiles', type=str, default='out', help='File name for output')
# Choose debug method 
parser.add_argument('--debug', action='store_true', help='Turn on debug mode.')
# Choose to build graph
parser.add_argument('--graph', action='store_true', help='Turn on debug mode.')

args = parser.parse_args()

if args.debug:
    Logger.debug=True

runExperiments()
output(args.outputFiles)

