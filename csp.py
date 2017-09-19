#!/usr/bin/python

import copy
import itertools

class CSP:
    def __init__(self):
        self.variables = []
        self.domains = {}
        self.constraints = {} # list of filter functions for each arc

    def add_variable(self, name, domain):
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}


    def get_all_arcs(self):
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var):
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, i, j, fn):
        if not j in self.constraints[i]:
            self.constraints[i][j] = []
        self.constraints[i][j].append(fn)

    def select_minimum_remaining_variable(self, assignment):
        minimum = float("inf")
        min_variable = False
        for key, value in assignment.iteritems():
            if len(value) > 1:
                if len(value) < minimum:
                    minimum = len(value)
                    min_variable = key
        return min_variable

    def is_solution(self, assignment):
        for variable in self.variables:
            if len(assignment[variable]) != 1:
                return False
        return True

    def is_solvable(self, assignment):
        for variable in self.variables:
            if len(assignment[variable]) == 0:
                return False
        return True

    def get_solution(self):
        assignment = copy.deepcopy(self.domains)
        # Run domain_filtering on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.domain_filtering(assignment, self.get_all_arcs())
        if self.is_solution(assignment):
            return assignment

        # Different search approaches to find a
        return self.greedy_best_first(assignment)
        #return self.bfs(assignment)
        #return self.dfs(assignment)

    def dfs(self, root):
        closed_set, queue = [], [root]
        while queue:
            current = queue.pop()
            self.domain_filtering(current, self.get_all_arcs())
            if self.is_solution(current):
                return current
            if self.is_solvable(current):
                for variable in self.variables:
                    for value in current[variable]:
                        new_assignment = copy.deepcopy(current)
                        new_assignment[variable] = [value]
                        if new_assignment not in closed_set:
                            closed_set.append(new_assignment)
                            queue.append(new_assignment)

    def bfs(self, root):
        closed_set, queue = [], [root]
        while queue:
            current = queue.pop(0)
            self.domain_filtering(current, self.get_all_arcs())
            if self.is_solution(current):
                return current
            if self.is_solvable(current):
                for variable in self.variables:
                    for value in current[variable]:
                        new_assignment = copy.deepcopy(current)
                        new_assignment[variable] = [value]
                        if new_assignment not in closed_set:
                            closed_set.append(new_assignment)
                            queue.append(new_assignment)

    def greedy_best_first(self, assignment):
        var = self.select_minimum_remaining_variable(assignment) # select variable not assigned any value yet
        if not var: # all variables have been assigned a single value
            return assignment
        for value in assignment[var]: # for every value in the domain for var
            new_assignment = copy.deepcopy(assignment) # copy assignment such that backtracking works
            new_assignment[var] = [value] # assign value to variable
            if self.domain_filtering(new_assignment, self.get_all_neighboring_arcs(var)): # checks arc consistency for var
                result = self.greedy_best_first(new_assignment) # call brecursively with new_assignment
                if result:
                    return result # if we have a result return it
        return False # no values can be assigned to var.


    def domain_filtering(self, assignment, queue):
        while queue: # while queue has elements
            i, j = queue.pop(0) # select first element in arc queue
            revised = self.revise(assignment, i, j) # checks if arc is consistent
            if revised:
                if len(assignment[i]) == 0: # if not value options left
                    return False
                for neighbor in self.get_all_neighboring_arcs(i):
                    # arc was not consistent all neighboring arcs therfore need to be arc-consistent checked again
                    if not neighbor == j: # avoids that current arc is added to queue
                        queue.append(neighbor)
        return True


    def revise(self, assignment, i, j):
        revised = False
        for x in assignment[i]: # for every value in current domain for i
            satisfiable = False
            for y in assignment[j]: # for every value in current domain for j
                for filter_function in self.constraints[i][j]:
                    if filter_function(i,j,(x,y)):
                        satisfiable = True # assigned value is satisfiable
                        break
                if satisfiable:
                    break
            if not satisfiable: # value is not satisfiable
                assignment[i].remove(x) # remove value from assignment
                revised = True # revise function did indeed remove a unvalid value from assignment.
        return revised
