#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 11:23:30 2017

@author: tac
"""

class Variable:

    def __init__(self):
        self.value = 0
        self.pos_list = list()
        self.neg_list = list()

class Clause:

    def __init__(self,lit_list):
        self.open = len(lit_list)
        self.subsumer = 0
        self.lit_list = list.copy(lit_list)


class Formula:
    # open_var       the number of open (unassigned) variables
    # open_cl        the number of open (not subsumed) clauses
    # clause_list    the list of Clause objects
    # variable_list  the list of Variable objects
    # unit_cl_list   the list of unit clauses
    # emtpy_cl_list  the list of empty clauses

    def __init__(self, kb,kb_dict,symbols,numb):
        # Initialize clause list, unit list and empty clauses list
        self.clause_list = list()
        self.unit_cl_list = list()
        self.empty_cl_list = list()
        # Read clause from DIMACS file
        self.kb_cnf(kb,kb_dict,symbols,numb)
        # Initially, all clauses are open
        self.open_cl = len(self.clause_list)
        return

    def kb_cnf(self,kb,kb_dict,symbols,numb):
        # Initially, all variables are open
        self.open_var = len(symbols);
        # NOTICE: variable indexes start from 1, not from 0
        self.variable_list = [Variable() for x in range(self.open_var + 1)]
        for i in range(0,len(kb.clauses)):
            clause = []
            lit_list = repr(kb.clauses[i]).split('(')
            if(len(lit_list) >1 ):
                lit_list = lit_list[-1].split(')')
                lit_list.pop()
                lit_list = lit_list[0].split('|')
                i = 0
                imax = len(lit_list)-1
                for lit in lit_list:
                    if((i==0) & (lit[0] =="~")):
                        clause.append(-kb_dict[lit[1:-1]])
                    elif((i==imax) & (lit[1] =="~")):
                        clause.append(-kb_dict[lit[2:]])
                    elif((i==imax)):
                        clause.append(kb_dict[lit[1:]])
                    elif((i==0)):
                        clause.append(kb_dict[lit[0:-1]])
                    elif(lit[1] =="~"):
                        clause.append(-kb_dict[lit[2:-1]])
                    else:
                        clause.append(kb_dict[lit[1:-1]])
                    i+=1
            else:
                if(lit_list[0][0] =="~"):
                    clause.append(-kb_dict[lit_list[0][1:]])
                else:
                    clause.append(kb_dict[lit_list[0]])
            
            clause2 = Clause(clause)
            cl_index = len(self.clause_list)
            # The clause is added to the clause list
            self.clause_list.append(clause2)
            # Variables must know where they occur positively or negatively
            for l in clause:
                v_index = abs(l)
                if (l > 0):
                    self.variable_list[v_index].pos_list.append(cl_index)
                else:
                    self.variable_list[v_index].neg_list.append(cl_index)
            # If the clause is unary, then it is added to the list
            if (len(clause) == 1):
                self.unit_cl_list.append(cl_index)
        return

    def is_satisfied(self):
        return (self.open_cl == 0)

    def is_contradicted(self):
        return (len(self.empty_cl_list) > 0)

    def do_eval(self, v_index, value):
        v = self.variable_list[v_index]
        if (value > 0):
            self.do_subsume(v_index, v.pos_list)
            self.do_simplify(v_index, v.neg_list)
        elif (value < 0):
            self.do_subsume(v_index, v.neg_list)
            self.do_simplify(v_index, v.pos_list)
        else:
            # value == 0: Cannot re-assign a value
            return
        v.value = value
        self.open_var = self.open_var - 1
        return

    def undo_eval(self, v_index):
        v = self.variable_list[v_index]
        if (v.value > 0):
            self.undo_subsume(v_index, v.pos_list)
            self.undo_simplify(v_index, v.neg_list)
        elif (v.value < 0):
            self.undo_subsume(v_index, v.neg_list)
            self.undo_simplify(v_index, v.pos_list)
        else:
             # v.value == 0: Cannot undo what has not been done
            return
        v.value = 0
        self.open_var = self.open_var + 1
        return

    def do_subsume(self, v_index, cl_index_list):
        for cl_index in cl_index_list:
            cl = self.clause_list[cl_index]
            # Check that we are subsuming the clause for the first time
            if (cl.subsumer == 0):
                cl.subsumer = v_index
                self.open_cl = self.open_cl - 1
        return

    def undo_subsume(self, v_index, cl_index_list):
        for cl_index in cl_index_list:
            cl = self.clause_list[cl_index]
            # Check that we are undoing the assignment to the first subsumer
            if (cl.subsumer == v_index):
                cl.subsumer = 0
                self.open_cl = self.open_cl + 1
        return

    def do_simplify(self, v_index, cl_index_list):
        for cl_index in cl_index_list:
            cl = self.clause_list[cl_index]
            # Check that the clause is not subsumed
            if (cl.subsumer == 0):
                cl.open = cl.open - 1
                if (cl.open == 0):
                    self.empty_cl_list.append(cl_index)
                elif (cl.open == 1):
                    self.unit_cl_list.append(cl_index)
        return

    def undo_simplify(self, v_index, cl_index_list):
        for cl_index in cl_index_list:
            cl = self.clause_list[cl_index]
            if (cl.subsumer == 0):
                cl.open = cl.open + 1
        return

    def do_print(self):
        v_index = 0
        print("VARIABLES")
        for v in self.variable_list:
            print(v_index,":",v.value,v.pos_list,v.neg_list)
            v_index = v_index + 1
        print("Open:",self.open_var)
        print("\nCLAUSES")
        for cl in self.clause_list:
            print("clause",":(",cl.open,",",cl.subsumer,"):",cl.lit_list)
        print("Open:",self.open_cl)
        print("\nUNIT CLAUSES")
        for cl_index in self.unit_cl_list:
            print(cl_index,end=' ')
        print("\n\nEMPTY CLAUSES")
        for cl_index in self.empty_cl_list:
            print(cl_index,end= ' ')
        print()
