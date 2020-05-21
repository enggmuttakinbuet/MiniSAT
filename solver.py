#!/usr/bin/python

import sys
import random
import copy
from collections import defaultdict


class DP(object):
    '''Class for Davis-Putnam solver.
    '''

    def __init__(self, file):
        self.file = file
        self.count = 0



    def solver(self, clauses):
        '''Main method of solver.

        Arguments:
            clauses {list} -- list of clauses

        Returns:
            dict -- dictionary of variables with assigned values
        '''

        # print('|START count:', self.count)
        # print('start:', clauses)
        clauses = self.pure_literals(clauses)
        # print('after pure:', clauses)
        clauses = self.unit_clauses(clauses)
        # print('after unit:', clauses)
        if [] in clauses:
            # print('false')
            return False
        if len(clauses) == 0:
            # print('success!')
            return self.vars
        split_var = self.JW_prob_split(clauses)
        self.count += 1
        # print(split_var)
        tmp = copy.deepcopy(clauses)
        assignment = self.solver(self.remove_clauses(split_var, clauses))
        if assignment is False:
            # print('backtracking...')
            self.count += 1
            clauses = copy.deepcopy(tmp)
            assignment = self.solver(self.remove_clauses(-split_var, clauses))
        if assignment is False:
            return False
        return self.vars



    def remove_clauses(self, variable, clauses):
        '''Update the list of clauses with the given variable assigned.

        Arguments:
            variable {int} -- variable with assgined value
            clauses {list} -- list of clauses

        Returns:
            list -- updated list of clauses
        '''

        new_clauses = []
        if variable >= 0:
            self.vars[variable] = True
        else:
            self.vars[abs(variable)] = False
        for clause in clauses:
            if variable in clause:
                continue
            else:
                if -variable in clause:
                    clause.remove(-variable)
                new_clauses.append(clause)
        return new_clauses

    def remove_clauses_testing_only(self, variable, clauses):
        '''Update the list of clauses with the given variable assigned.

        Arguments:
            variable {int} -- variable with assgined value
            clauses {list} -- list of clauses

        Returns:
            list -- updated list of clauses
        '''

        print('variable:', variable)
        print('number of clauses:', len(clauses))
        new_clauses = []
        if variable >= 0:
            self.vars[variable] = True
        else:
            self.vars[abs(variable)] = False
        for clause in clauses:
            if variable in clause:
                continue
            else:
                if -variable in clause:
                    clause.remove(-variable)
                new_clauses.append(clause)
        return new_clauses

    def read(self):
        '''Method for reading the clauses from the input file.

        Returns:
            list -- list of clauses
        '''

        # Initialize clauses list.
        clauses = []

        # Initialize variables.
        vars_tmp = set()

        # Start reading from the file.
        with open(self.file, 'r') as input_file:
            for line in input_file:
                parsed = line.split()

                # Check whether it is valid line or supplementary line.
                if not parsed or parsed[0] == 'p' or parsed[0] == 'c':
                    continue
                else:
                    eff_parsed = parsed[:-1]
                    clause = set()
                    for lit in eff_parsed:
                        lit = int(lit)
                        clause.add(lit)

                        # Collect variable.
                        abs_lit = abs(lit)
                        vars_tmp.add(abs_lit)
                    clauses.append(list(clause))

        # Initialize all collected variables, e.g. {'115': [False] ...} - where [truth_val]
        self.vars = dict.fromkeys(vars_tmp, False)
        return clauses

    def tautology(self, clauses):
        '''Check and remove tautology from the list of clauses.

        Returns:
            list -- list of clauses
        '''

        new_clauses = []
        check = 1
        for clause in clauses:
            for lit in clause:
                if -lit in clause:
                    check = 0
                    break
            if check == 1:
                new_clauses.append(clause)
            else:
                check = 1
        return new_clauses

    def pure_literals(self, clauses):
        '''Collect and remove the pure literals from the list of clauses.

        Returns:
            list -- list of clauses
        '''

        p_lits = set()
        non_p_lits = set()
        for clause in clauses:
            for lit in clause:
                neg_lit = -lit
                abs_lit = abs(lit)
                if neg_lit not in p_lits:
                    if abs_lit not in non_p_lits:
                        p_lits.add(lit)
                else:
                    p_lits.remove(neg_lit)
                    non_p_lits.add(abs_lit)
        for lit in p_lits:
            clauses = self.remove_clauses(lit, clauses)
        return clauses

    def unit_clauses(self, clauses):
        '''Collect and remove unit clauses from the list of clauses.

        Returns:
            list -- list of clauses
        '''

        unit_var = set()
        for clause in clauses:
            if len(clause) == 1:
                unit_var.add(clause[0])
        while len(unit_var) > 0:
            for unit in unit_var:
                clauses = self.remove_clauses(unit, clauses)
            unit_var = set()
            clauses = self.unit_clauses(clauses)
        return clauses



    def JW_prob_split(self, clauses):
        '''Use probabilistic Jeroslow-Wang heuristic to split variable.

        Arguments:
            clauses {list} -- list of clauses

        Returns:
            int -- selected variable to split
        '''

        J = defaultdict(int)
        for clause in clauses:
            clause_len = len(clause)
            for lit in clause:
                J[lit] += 2 ** (-clause_len)

        choices = []
        vals = []
        for k in list(J):
            lit = abs(k)
            if lit not in choices:
                choices.append(lit)
                vals.append(J[k] + J[-k])

        split = random.choices(choices, weights=vals, k=1)
        split = split[0]

        split = random.choices([split, -split], weights=[J[split], J[-split]], k=1)
        split = split[0]
        return split


def main(argv):
    


    sat_solver = DP(argv[0])
    clauses = sat_solver.read()
    clauses = sat_solver.tautology(clauses)
    var = sat_solver.solver(clauses)

    if var is False:
        # print('Oops, the problem is not solvable...')
        print('s UNSATISFIABLE')

    else:
        # perfect resutl show print output
        # sat_solver.output_results(var)
        print('s SATISFIABLE')
        res="v"
        for k in list(var):
            if(var[k]):
                res+=" "+str(k)
            else:
                res+=" "+str(-k)
        res+=" 0\n"
        print(res)


if __name__ == '__main__':
    main(sys.argv[1:])
