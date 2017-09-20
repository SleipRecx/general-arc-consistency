import sys
import copy
import cProfile

import hashlib
import json

from gac import domain_filtering, is_solution, is_solvable
from nonogram import create_nonogram_csp, print_nonogram
from search import best_first_search


# Heuristics to select value that reduces domain most
def most_reducing_value(csp):
    variables, domains, constraints = csp
    value = 0
    for variable in variables:
        value += len(domains[variable])
    return value

# Heuristic to find variable with least possible values
def select_minimum_remaining_variable(csp):
    variables, domains, constraints = csp
    minimum = float("inf")
    min_variable = None
    for variable in variables:
        for domain in domains[variable]:
            domain_size = len(domain)
            if domain_size > 1 and domain_size < minimum:
                minimum = domain_size
                min_variable = variable
    return min_variable


def generate_successors(csp):
    # Generates all domain reduced successor for a csp state.
    variables, domains, constraints = csp
    successors = []

    # Loop over possible values for all variables
    for variable in variables:
        for value in domains[variable]:

            # Copy domain to prevent catastrophe
            assignment = copy.deepcopy(domains)

            # Make assumption
            assignment[variable] = [value]

            # Domain filter assumption
            assignment = domain_filtering(variables, assignment, constraints, print_nonogram)
            successor_state = (variables, assignment, constraints)
            if is_solvable(successor_state):
                successors.append(successor_state) # Only add solvable states
    return successors


# Hash csp state for closed sets
def hash_state(csp):
    variables, domains, constraints = csp
    return hashlib.sha1(json.dumps(domains, sort_keys=True)).hexdigest()


# Combination of best_first_search and GAC to that solves CSP's
def gac_and_best_first(variables, domains, constraints):

    # Reduce domains with GAC
    reduced_domains = domain_filtering(variables, domains, constraints, print_nonogram)

    # Pack problem into tuple such that it's ready for best-first search
    problem = (variables, reduced_domains, constraints)

    # Checks if CSP problem can be solved (no domains with zero values)
    if not is_solvable(problem):
        print 'No solution'

    # There is no need to search for an solution when domain filtering solves it.
    if is_solution(problem):
        print_nonogram(problem)
    else:
        # Search for a solution utilizing a general best-first algorithm
        result, generated, expanded = best_first_search(problem, hash_state, is_solution, generate_successors, most_reducing_value, print_nonogram)

        # Display Stats from search
        print_nonogram(result)
        print "Generated Nodes", generated
        print "Expanded Nodes", expanded

# Read puzzle name
puzzle = str(sys.argv[1])

# Create CSP problem
variables, assignment, constraints = create_nonogram_csp(puzzle)

# Run A* GAC to solve puzzle
gac_and_best_first(variables, assignment, constraints)
