import EthicsPlanner.Environment.GraphVisualiser as v
from EthicsPlanner.Planner.Solution import BestSubGraph
from datetime import datetime
import os
import sys
import pandas as pd



def record_LAO(mdp, bpsg, solver, TC, time, horizon, algorithm, filename="Results.txt"):
    # Results
    new_row = {}
    new_row['DateTime'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    new_row['expanded'] = len(bpsg.expandedStates)
    new_row['solution size'] = len(bpsg.states)
    new_row['action revisions'] = solver.revisions
    new_row['Time'] = time
    new_row['Horizon'] = horizon
    new_row['algorithm'] = algorithm
    new_row['Theories'] = TC

    r = "LAO. Theories {tc} Run: {dt}\n".format(tc = str(TC), dt = new_row['DateTime'])
    r += 'Expanded {n} states\n'.format(n=new_row['expanded'])
    r += 'Solution graph has {n} states.\n'.format(n=new_row['solution size'])
    r += 'Time taken {t}\n'.format(t=time)
    r += 'Action revisions: {n}\n'.format(n=new_row['action revisions'])
    
    count_theories(mdp, new_row, bpsg.V, bpsg.pi, r)
    
    pol =  count_actions(bpsg, mdp, new_row)

    r+="\n Lies: {l}\n Honest: {h}\n Positive: {p}\n Negative: {n}\n\n".format(l=new_row['lies'], n=new_row['hons'], p=new_row['pos'], h=new_row['neg'])
    r+=pol
    r+="\n\n\n"
    
    f = open(os.getcwd() + '/{fn}.txt'.format(fn=filename), 'a')
    f.write(r)
    f.close()

    excel_write(new_row, filename)
    return new_row

def record_VI(mdp, pi, solver, TC, time, horizon, algorithm, filename="Results.txt"):
    
    new_row = {}
    new_row['DateTime'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    new_row['expanded'] = len(mdp.states)
    new_row['action revisions'] = solver.revisions
    new_row['Time'] = time
    new_row['Horizon'] = horizon
    new_row['algorithm'] = algorithm
    new_row['Theories'] = TC
    
    bpsg = BestSubGraph(0, mdp=mdp)
    bpsg.pi = pi
    bpsg.update(mdp)
    pol = count_actions(bpsg, mdp, new_row)
    new_row['solution size'] = len(bpsg.states)

    
    r = "VI. Theories {tc} Run: {dt}\n".format(tc = str(TC), dt = new_row['DateTime'])
    r += 'Expanded {n} states\n'.format(n=new_row['expanded'])
    r += 'Solution graph has {n} states.\n'.format(n=new_row['solution size'])
    r += 'Time taken {t}\n'.format(t=time)
    r += 'Action revisions: {n}\n'.format(n=new_row['action revisions'])
    
    count_theories(mdp, new_row, solver.V, pi, r)

    r+="\n Lies: {l}\n Honest: {h}\n Positive: {p}\n Negative: {n}\n\n".format(l=new_row['lies'], n=new_row['hons'], p=new_row['pos'], h=new_row['neg'])
    r+=pol
    r+="\n\n\n"

    f = open(os.getcwd() + '/{fn}.txt'.format(fn=filename), 'a')
    
    f.write(r)
    f.close()
    
    excel_write(new_row, filename)
    


def count_theories(mdp, d, V, pi, r):
    startState = mdp.states[0]
    for t in mdp.Theories:
        e = t.Gather(mdp.getActionSuccessors(startState, pi[startState.id], readOnly=True), V[t.tag])
        d[t.tag] = e
        r+= '{theory} final estimation={g}\n'.format(theory=t.tag, g=t.EstimateString(e))
    r+= '\n Policy: \n'


def count_actions(bpsg, mdp, d):
    d['neg'], d['pos'], d['lies'], d['hons'] = 0,0,0,0
    pol=""
    for s in bpsg.states:
        if s in bpsg.pi.keys():
            pol+="({id},{a})\n".format(id=s, a=bpsg.pi[s])
            if 'neg' in bpsg.pi[mdp.states[s].id]:
                d['neg']+=1
            if 'pos' in bpsg.pi[mdp.states[s].id]:
                d['pos']+=1
            if 'lie' in bpsg.pi[mdp.states[s].id]:
                d['lies']+=1
            if 'hon' in bpsg.pi[mdp.states[s].id]:
                d['hons']+=1
    return pol

def excel_write(new_row, filename):
    df = 0
    try:
        df = pd.read_csv(os.getcwd() + '/{fn}.csv'.format(fn=filename))
    except:
        df = pd.DataFrame(columns=['DateTime', 'Horizon', 'utility', 'absolute', 'wellbeing', 'expanded', 'solution size', 'Time', 'action revisions', 'lies', 'hons', 'pos', 'neg', 'Theories'])

    df.loc[len(df)] = new_row
    print(df.head())
    df.to_csv(os.getcwd() + '/{fn}.csv'.format(fn=filename),index=0)