import copy
import itertools
import sys
import threading
import time
import cProfile

from random import choice
import sys
from csp import CSP

def print_solution(result):
    if result == False:
        print 'No solution'
        return
    sorted_keys = []
    for key in result.keys():
        if "R" in key:
            sorted_keys.append(int(key[1:]))
    sorted_keys.sort()
    for key in sorted_keys:
        for bit in result['R' + str(key)][0]:
            if bit == 1:
                print '\033[0;103m' + " " + '\033[0m',
            else:
                print ' ',
        print

def create_domain(length, specifications):
    domain = []
    min_placement = []
    for s in specifications:
        for i in range(s):
            min_placement.append(1)
        min_placement.append(0)
    min_placement.pop(len(min_placement) - 1)

    insert_indices = [i + 1 for i, x in enumerate(min_placement) if x == 0]
    insert_indices.extend([0, len(min_placement)])
    combinations = itertools.combinations_with_replacement(insert_indices, length - len(min_placement))
    for c in combinations:
        result = min_placement[:]
        insert_positions = list(c)
        insert_positions.sort()
        offset = 0
        for index in insert_positions:
            result.insert(index + offset, 0)
            offset += 1
        domain.append(result)
    return domain


def filter_function(var1, var2, value_pair):
    var1 = int(var1[1:])
    var2 = int(var2[1:])
    row, col = value_pair
    return row[var2] == col[var1]

def is_valid_row_col_combination(row, col, row_number, col_number):
    return row[col_number] == col[row_number]

def one_inference_loop(csp):
    assignment = copy.deepcopy(csp.domains)
    csp.print_domain_size(assignment)
    csp.inference(assignment, csp.get_all_arcs(), filter_function)
    print '----------------------------------------------'
    csp.print_domain_size(assignment)

def create_nonogram_csp(filename):
    f = open(filename,'r')
    lines = f.read().split("\n")
    lines[0] = lines[0].split()

    number_of_cols = int(lines[0][0])
    number_of_rows =  int(lines[0][1])

    row_spec = [row for row in lines[1:number_of_rows + 1]][::-1]
    col_spec = [col for col in lines[len(lines) - 1 - number_of_cols:len(lines) - 1]]

    csp = CSP()

    csp.filter_functions.append(filter_function)
    print csp.filter_functions[0]('R0', 'C0',)
    
    for i in range(len(row_spec)):
        segment_specification = map(int, list(row_spec[i].split()))
        domain = create_domain(number_of_cols, segment_specification)
        csp.add_variable("R" + str(i), domain)

    for i in range(len(col_spec)):
        constraints = map(int, list(col_spec[i].split()))
        domain = create_domain(number_of_rows, constraints)
        csp.add_variable("C" + str(i), domain)

    row_variables = filter(lambda x: 'R' in x, csp.variables)
    col_variables = filter(lambda x: 'C' in x, csp.variables)

    for (row, col) in itertools.product(row_variables, col_variables):
        csp.add_all_different_constraint([row, col])
    return csp


puzzle = str(sys.argv[1])
csp = create_nonogram_csp(puzzle)
solution = csp.backtracking_search(filter_function)
print_solution(solution)
#print 'Backtracks', csp.b_counter
#cProfile.run('csp.backtracking_search(filter_function)')
