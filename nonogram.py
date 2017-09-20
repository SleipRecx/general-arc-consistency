import sys
import copy
import itertools
import cProfile

"""
 This file is dedicated to converting nonograms (Griddlers)
 into Constraint Satisfaction Problems (CSPs)
"""
def create_nonogram_csp(filename):

    # Read file with nonogram specifications
    f = open(filename,'r')
    lines = f.read().split("\n")
    lines[0] = lines[0].split()

    number_of_cols = int(lines[0][0])
    number_of_rows =  int(lines[0][1])

    row_spec = [row for row in lines[1:number_of_rows + 1]][::-1]
    col_spec = [col for col in lines[len(lines) - 1 - number_of_cols:len(lines) - 1]]

    # Finished reading file, time to turn this into a CSP problem

    variables = []
    domains = {}
    constraints = {}

    # Add all rows and their domain
    for i in range(len(row_spec)):
        segment_specification = map(int, list(row_spec[i].split()))
        domain = generate_domains_from_specifications(number_of_cols, segment_specification)
        variable = "R" + str(i)

        variables.append(variable)
        domains[variable] = domain
        constraints[variable] = {}

    # Add all cols and their domain
    for i in range(len(col_spec)):
        segment_specification = map(int, list(col_spec[i].split()))
        domain = generate_domains_from_specifications(number_of_rows, segment_specification)
        variable = "C" + str(i)

        variables.append(variable)
        domains[variable] = domain
        constraints[variable] = {}

    # Only thing left now is creating some constraints betwen rows and cols
    row_variables = filter(lambda x: 'R' in x, variables)
    col_variables = filter(lambda x: 'C' in x, variables)


    for (row, col) in itertools.product(row_variables, col_variables):
        constraints[row][col] = compatible_value_pair
        constraints[col][row] = compatible_value_pair

    # Return nonogramp represented as a CSP
    return (variables, domains, constraints)

def generate_domains_from_specifications(length, specifications):
    # Clever function to generate possible domains for a rows and cols

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

# takes a row and a column and checks if the value where they meet is the same
def compatible_value_pair(i, j, value_pair):
    x, y = value_pair
    x_index = int(i[1:])
    y_index = int(j[1:])
    return x[y_index] == y[x_index]

# Prints nonogram to console
def print_nonogram(result):
    variables, domains, constraints = result
    sorted_keys = []
    for key in domains.keys():
        if "R" in key:
            sorted_keys.append(int(key[1:]))
    sorted_keys.sort()
    for key in sorted_keys:
        for bit in domains['R' + str(key)][0]:
            if bit == 1:
                print '\033[0;103m' + " " + '\033[0m',
            else:
                print ' ',
        print
    print
