def domain_filtering(variables, domains, constraints, print_state):
    queue = get_all_arcs(constraints)
    while queue: # while queue has elements
        i, j = queue.pop(0) # select first element in arc queue
        revised = revise(variables, domains, constraints, i, j) # checks if arc is consistent
        if revised:
            # print_state((variables, domains, constraints))
            for (k, i) in get_all_neighboring_arcs(constraints, i):
                # arc was not consistent all neighboring arcs therfore need to be arc-consistent checked again
                if k != i:
                    queue.append((k, i))
    return domains

def revise(variables, domains, constraints, i, j):
    revised = False
    for x in domains[i]: # for every value in current domain for i
        satisfiable = False
        for y in domains[j]: # for every value in current domain for j
            filter_function = constraints[i][j]
            if filter_function(i,j,(x,y)):
                satisfiable = True # assigned value is satisfiable
                break
        if not satisfiable: # value is not satisfiable
            domains[i].remove(x) # remove value from domains
            revised = True # revise function did indeed remove a unvalid value from domains.
    return revised


def get_all_arcs(constraints):
    # Returns all arcs in problem
    return [(i, j) for i in constraints for j in constraints[i]]


def get_all_neighboring_arcs(constraints, variable):
    # Returns only arcs where given variable is present.
    result = [(i, variable) for i in constraints[variable]]
    result.extend([(variable, i) for i in constraints[variable]])
    return result

def is_solution(csp):
    # If all domains have a single value the csp is solved.
    variables, domains, constraints = csp
    for key, value in domains.iteritems():
        if len(value) != 1:
            return False
    return True

def is_solvable(csp):
    variables, domains, constraints = csp
    # If any domain has zero possible values the csp is unsolvable.
    for key, value in domains.iteritems():
        if len(value) == 0:
            return False
    return True
