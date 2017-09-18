#!/usr/bin/python

import copy
import itertools
import sys
import time

from random import choice

class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        self.constraints = {}

        self.filter_functions = []

        self.b_counter = 0
        self.f_counter = 0


    def add_variable(self, name, domain):
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def print_domain_size(self, assignment = None):
        if assignment == None:
            assignment = self.domains
        for var in self.variables:
            print var + ": " + str(len(assignment[var]))

    def get_all_possible_pairs(self, a, b):
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, i, j):
        if j not in self.constraints[i]:
            # Get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])


    def add_all_different_constraint(self, variables):
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j)

    def select_minimum_remaining_variable(self, assignment):
        minimum = float("inf")
        min_variable = None
        for key, value in assignment.iteritems():
            if len(value) > 1:
                if len(value) < minimum:
                    minimum = len(value)
                    min_variable = key
        if not min_variable:
            return False
        return min_variable


    def backtracking_search(self, filter_function):
        assignment = copy.deepcopy(self.domains)
        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs(), filter_function)
        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment, filter_function)

    def backtrack(self, assignment, filter_function):
        self.b_counter += 1 # increment backtrack counter
        var = self.select_minimum_remaining_variable(assignment) # select variable not assigned any value yet
        if not var: # all variables have been assigned a single value
            return assignment
        for value in assignment[var]: # for every value in the domain for var
            new_assignment = copy.deepcopy(assignment) # copy assignment such that backtracking works
            new_assignment[var] = [value] # assign value to variable
            if self.inference(new_assignment,self.get_all_neighboring_arcs(var), filter_function): # checks arc consistency for var
                result = self.backtrack(new_assignment, filter_function) # call backtrack recursively with new_assignment
                if result:
                    return result # if we have a result return it
        self.f_counter += 1 # increment backtrack_failure counter
        return False # no values can be assigned to var.


    def inference(self, assignment, queue, filter_function):
        while queue: # while queue has elements
            i, j = queue.pop(0) # select first element in arc queue
            if self.revise(assignment, i, j, filter_function): # checks if arc is consistent
                if len(assignment[i]) == 0: # if not value options left
                    return False #
                for neighbor in self.get_all_neighboring_arcs(i):
                    # arc was not consistent all neighboring arcs therfore need to be arc-consistent checked again
                    if not neighbor == j: # avoids that current arc is added to queue
                        queue.append(neighbor)
        return True # returns true when queue is empty


    def revise(self, assignment, i, j, filter_function):
        revised = False # initialize revised to False
        for x in assignment[i]: # for every value in current domain for i
            satisfiable = False
            for y in assignment[j]: # for every value in current domain for j
                if filter_function(i, j, (x, y)):
                    satisfiable = True # assigned value is satisfiable
                    break
            if not satisfiable: # value is not satisfiable
                assignment[i].remove(x) # remove value from assignment
                revised = True # revise function did indeed remove a unvalid value from assignment.
        return revised
