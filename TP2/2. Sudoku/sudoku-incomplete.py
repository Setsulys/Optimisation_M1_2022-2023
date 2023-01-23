#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools
import sys
import os
"""Sudoku"""

def var(i,j,k):
    """Return the literal Xijk.
    """
    return (1,i,j,k)

def neg(l):
    """Return the negation of the literal l.
    """
    (s,i,j,k) = l
    return (-s,i,j,k)

def initial_configuration():
    """Return the initial configuration of the example in td6.pdf
    
    >>> cnf = initial_configuration()
    >>> [(1, 1, 4, 4)] in cnf
    True
    >>> [(1, 2, 1, 2)] in cnf
    True
    >>> [(1, 2, 3, 1)] in cnf
    False
    """
    return [[var(1,4,4)],[var(2,1,2)],[var(3,2,1)],[var(4,3,1)]]

def at_least_one(L):
    """Return a cnf that represents the constraint: at least one of the
    literals in the list L is true.
    
    >>> lst = [var(1, 1, 1), var(2, 2, 2), var(3, 3, 3)]
    >>> cnf = at_least_one(lst)
    >>> len(cnf)
    1
    >>> clause = cnf[0]
    >>> len(clause)
    3
    >>> clause.sort()
    >>> clause == [var(1, 1, 1), var(2, 2, 2), var(3, 3, 3)]
    True
    """
    return [[x for x in L if x[0]==1]]

def at_most_one(L):
    """Return a cnf that represents the constraint: at most one of the
    literals in the list L is true
    
    >>> lst = [var(1, 1, 1), var(2, 2, 2), var(3, 3, 3)]
    >>> cnf = at_most_one(lst)
    >>> len(cnf)
    3
    >>> cnf[0].sort()
    >>> cnf[1].sort()
    >>> cnf[2].sort()
    >>> cnf.sort()
    >>> cnf == [[neg(var(1,1,1)), neg(var(2,2,2))], \
    [neg(var(1,1,1)), neg(var(3,3,3))], \
    [neg(var(2,2,2)), neg(var(3,3,3))]]
    True
    """
    return [[neg(x),neg(y)] for x, y in itertools.combinations(L,2)]

def assignment_rules(N):
    """Return a list of clauses describing the rules for the assignment (i,j) -> k.
    """
    cnf = []
    for i in range(1,N+1):
        for j in range(1,N+1):
            elt = [var(i,j,k) for k in range(1,N+1)]
            cnf.extend(at_least_one(elt))
            cnf.extend(at_most_one(elt))
    return cnf

def row_rules(N):
    """Return a list of clauses describing the rules for the rows.
    """
    cnf = []
    for i in range(1,N+1):
        for k in range(1,N+1):
            elt = [var(i,j,k) for j in range(1,N+1)]
            cnf.extend(at_least_one(elt))
            cnf.extend(at_most_one(elt))
    return cnf

def column_rules(N):
    """Return a list of clauses describing the rules for the columns.
    """
    cnf = []
    for j in range(1,N+1):
        for k in range(1,N+1):
            elt = [var(i,j,k) for i in range(1,N+1)]
            cnf.extend(at_least_one(elt))
            cnf.extend(at_most_one(elt))
    return cnf

def subgrid_rules(N):
    """Return a list of clauses describing the rules for the subgrids.
    """
    cnf = []
    sqrt = int(N ** 0.5)
    for i in range(1, sqrt + 1):
        for j in range(1, sqrt + 1):
            for k in range(1,N+1):
                elt = []
                for i_prim in range((i - 1) * sqrt + 1, i * sqrt + 1):
                    for j_prim in range((j - 1) * sqrt + 1, j * sqrt + 1):
                        elt.append(var(i_prim,j_prim,k))
                cnf.extend(at_least_one(elt))
                cnf.extend(at_most_one(elt))
    return cnf

def generate_rules(N):
    """Return a list of clauses describing the rules of the game.
    """
    cnf = []    
    cnf.extend(assignment_rules(N))
    cnf.extend(row_rules(N))
    cnf.extend(column_rules(N))
    cnf.extend(subgrid_rules(N))
    return cnf

def literal_to_integer(l, N):
    """Return the external representation of the literal l.

    >>> literal_to_integer(var(1,2,3), 4)
    7
    >>> literal_to_integer(neg(var(3,2,1)), 4)
    -37
    """
    s,i,j,k = l
    return s * (N ** 2 * (i - 1) + N * (j - 1) + k)

def repr_interne(file, representation, N):
    with open(file, "w") as f:
        final = "p cnf " + str(N**3) + " " + str(len(representation)) + "\n"
        for lst in representation:
            string = ""
            for truc in lst:
                string += str(literal_to_integer(truc, N)) + " "
            string += "0\n"
            final += string
        f.write(final)

def configuration_file(file):
    with open(file, "r") as f:
        size = int(f.readline())
        lines = []
        for i in range(size):
            lst = []
            for elem in f.readline().strip("\n").split(" "):
                lst.append(int(elem))
            lines.append(lst)
        conf = []
        for i in range(size):
            line = []
            for j in range(size):
                if(lines[i][j] != 0):
                    line.append(var(i + 1, j + 1, lines[i][j]))
            conf.extend(at_least_one(line))
            conf.extend(at_most_one(line))
    conf.extend(generate_rules(size))
    repr_interne("output.cnf",conf, size)
    os.system("minisat -verb=0 output.cnf output.out")
    with open("output.out", "r") as f:
        f.readline()
        line = f.readline().strip("\n").split(" ")
        line = [int(x) for x in line[:-1]]
        lst = []

        for index, value in enumerate(line):
            if value > 0:
                if((index + 1) % size == 0):
                    lst.append(size)
                else:
                    lst.append((index + 1) % size)
            if abs(value) % (size ** 2) == 0 and index != 0:
                string = ""
                for elem in lst:
                    string += str(elem) + " "
                print(string)
                lst = []
        string = ""
        for elem in lst:
            string += str(elem) + " "
        print(string)

def main():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    main()
    if(len(sys.argv) == 2):
        configuration_file(sys.argv[1])
    else:
        print("Erreur, pas le bon nombre d'arguments.")