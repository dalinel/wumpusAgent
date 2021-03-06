#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 11:32:47 2017

@author: tac
"""
import random
class Status:
    def __init__(self):
        self.var_index = 0
        self.closed = False
    def __init__(self, var_index, closed):
        self.var_index = var_index
        self.closed = closed
        
def fast_dpll(formula, choose_variable):
    stack = list()
    done = False
    while (not done):
        # Assign all unit clauses, including those that are generated by this process
        unit_propagate(formula, stack)
        if formula.is_satisfied():
            # The formula is satisfied: end of search
            done = True
        elif formula.is_contradicted():
            # The formula is contraticted: keep searching if possible, otherwise give up
            done = backtrack(formula, stack)
        else:
            # We must choose a variable and assign it tentatively
            choose_variable(formula, stack)
    return extract_assignment(formula, stack)

def unit_propagate(formula, stack):
    # While there is at least one unit clause...
    while (len(formula.unit_cl_list) > 0):
        # ... get the unit clause 
        cl_index = formula.unit_cl_list.pop()
        cl = formula.clause_list[cl_index]
        for lit in cl.lit_list:
            # Search the variable still unassigned (if any)
            var = formula.variable_list[abs(lit)]
            if (var.value == 0):
                # Assign the variable so as to subsume the clause
                formula.do_eval(abs(lit), lit/abs(lit))
                # Record the assignemnt in the stack as "closed"
                stack.append(Status(abs(lit),True))
                break
    return

def backtrack(formula, stack):
    # Reset the empty clause list
    formula.empty_cl_list.clear()
    # Go back in the stack, search for an "open" assigment
    while (len(stack) > 0):
        sr = stack.pop()
        # Get the variable index
        var_index = sr.var_index
        # The new value to assign, if any, is the opposite of the current one
        new_value = -1 * formula.variable_list[var_index].value
        # Undo the old assignment
        formula.undo_eval(var_index)
        if (not sr.closed):
            # Redo assignment with new value when possible
            formula.do_eval(var_index, new_value)
            # The assignment is now "closed": no further values to try
            stack.append(Status(var_index,True))
            # Backtracking was successful: the search must go on
            return False
    # No further backtracking is possible: the search must end
    return True

def extract_assignment(formula, stack):
    assignment = list()
    for sr in stack:
        value = formula.variable_list[sr.var_index].value
        assignment.append(sr.var_index * value)
    return assignment
    
def choose_variable_at_random(formula, stack):
    if (formula.open_var > 1):
        num = random.randint(1,formula.open_var)
    else:
        num = 1
    for var_index in range(1,len(formula.variable_list)):
        v = formula.variable_list[var_index]
        if (v.value == 0):
            num = num - 1
            if (num == 0):
                value = [-1,1][random.randint(0,1)]
                formula.do_eval(var_index, value)
                stack.append(Status(var_index,False))
                break
    return
