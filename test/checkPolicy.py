

def check(mdp, solStateTiles, solActions, pi):
    solStates = {}
    for s in mdp.states:
        if s.props['tile'] in solStateTiles:
            solStates[solStateTiles.index(s.props['tile'])] = s

    assert len(solStates) == len(solStateTiles)

    for idx, s in solStates.items():
        assert pi[s.id] == str(solActions[idx])