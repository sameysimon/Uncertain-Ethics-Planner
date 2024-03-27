def dfs(graph, state, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(state)
    path.append(state)

    successors = graph[state]

    result_dict = {}

    for action, next_states in successors.items():
        for next_state in next_states:
            if next_state not in visited:
                result_dict[(state, action)] = result_dict.get((state, action), []) + [path[:] + [next_state]]
                dfs(graph, next_state, visited, path)
    
    path.pop()

    return result_dict

def dfs_for_all_states(graph):
    result_dict = {}
    for state, actions in graph.items():
        for action in actions:
            dfs_result = dfs(graph, state)
            result_dict.update(dfs_result)
    return result_dict

# Example graph
graph = {
    'A': {'action1': ['B', 'C'], 'action2': ['D']},
    'B': {'action3': ['E']},
    'C': {'action4': ['F']},
    'D': {'action5': ['G']},
    'E': {'action6': ['H']},
    'F': {'action7': ['I']},
    'G': {},
    'H': {},
    'I': {}
}

# Perform DFS for all states and actions
result = dfs_for_all_states(graph)

# Print the result dictionary
for key, value in result.items():
    print(f"{key}: {value}")
