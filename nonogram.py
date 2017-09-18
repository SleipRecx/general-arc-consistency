import sys
import copy
import itertools
import cProfile
from csp import CSP

def print_nonogram(result):
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

def compatible_value_pair(i, j, value_pair):
    x, y = value_pair
    x_index = int(i[1:])
    y_index = int(j[1:])
    return x[y_index] == y[x_index]

def create_nonogram_csp(filename):
    f = open(filename,'r')
    lines = f.read().split("\n")
    lines[0] = lines[0].split()

    number_of_cols = int(lines[0][0])
    number_of_rows =  int(lines[0][1])

    row_spec = [row for row in lines[1:number_of_rows + 1]][::-1]
    col_spec = [col for col in lines[len(lines) - 1 - number_of_cols:len(lines) - 1]]

    csp = CSP()

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
        csp.add_constraint_one_way(row, col, compatible_value_pair)
        csp.add_constraint_one_way(col, row, compatible_value_pair)
    return csp


puzzle = str(sys.argv[1])
csp = create_nonogram_csp(puzzle)
solution = csp.get_solution()
print_nonogram(solution)
#print 'Backtracks', csp.b_counter
cProfile.run('csp.get_solution()')
