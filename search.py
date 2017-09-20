from collections import deque

# General breadth first search
def bfs(root, is_terminal, generate_successors):
    closed, queue = [], deque([root])
    while queue:
        current = queue.popleft()
        if is_terminal(current):
            return current
        for successor in generate_successors(current):
            if not successor in closed:
                queue.append(successor)
    return False

# General best first search, given it's params
def best_first_search(root, hash_state, is_terminal, generate_successors, heuristic, print_state):
    closed, queue = [], deque([root])
    generated = 0
    while queue:
        current = pop_best_state(queue, heuristic)
        if is_terminal(current):
            return (current, generated, len(closed))
        print_state(current)
        for successor in generate_successors(current):
            generated += 1
            if not hash_state(successor) in closed:
                closed.append(hash_state(successor))
                queue.append(successor)

    return False

# Returns best state from queue using provided heuristic
def pop_best_state(queue, heuristic):
    best_state = queue[0]
    best_h_cost = heuristic(best_state)
    for state in queue:
        h_cost = heuristic(state)
        if h_cost < best_h_cost:
            best_state = state
            best_h_cost = h_cost
    queue.remove(best_state)
    return best_state
