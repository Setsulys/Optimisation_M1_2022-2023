#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import sys
import os

"""Sudoku"""


def var(i, j, k):
    """Return the literal Xijk.
    """
    return (1, i, j, k)


def neg(l):
    """Return the negation of the literal l.
    """
    (s, i, j, k) = l
    return (-s, i, j, k)


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
    return [[(1, 1, 4, 4)], [(1, 2, 1, 2)], [(1, 3, 2, 1)], [(1, 4, 3, 1)]]


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
    return [L]


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
    return [[neg(L[a]), neg(L[b])] for a in range(len(L)) for b in range(a + 1, len(L))]


def assignment_rules(N):
    """Return a list of clauses describing the rules for the assignment (i,j) -> k.
    """
    cnf = []
    list_var = []
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            for n in range(1, N + 1):
                list_var.append(var(i, j, n))
            cnf.extend(at_least_one(list_var))
            cnf.extend(at_most_one(list_var))
            list_var = []
    return cnf


def row_rules(N):
    """Return a list of clauses describing the rules for the rows.
    """
    cnf = []
    list_var = []
    for i in range(1, N + 1):
        for n in range(1, N + 1):
            for j in range(1, N + 1):
                list_var.append(var(i, j, n))
            cnf.extend(at_least_one(list_var))
            cnf.extend(at_most_one(list_var))
            list_var = []
    return cnf


def column_rules(N):
    """Return a list of clauses describing the rules for the columns.
    """
    cnf = []
    list_var = []
    for j in range(1, N + 1):
        for n in range(1, N + 1):
            for i in range(1, N + 1):
                list_var.append(var(i, j, n))
            cnf.extend(at_least_one(list_var))
            cnf.extend(at_most_one(list_var))
            list_var = []
    return cnf


def subgrid_rules(N):
    """Return a list of clauses describing the rules for the subgrids.
    """
    cnf = []
    list_var = []
    racine_n = int(math.sqrt(N))
    for i in range(1, N + 1, racine_n):
        for j in range(1, N + 1, racine_n):
            for n in range(1, N + 1):
                for x in range(N):
                    list_var.append(var(i + int(x / racine_n), j + (x % racine_n), n))
                cnf.extend(at_most_one(list_var))
                cnf.extend(at_least_one(list_var))
                list_var = []
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
    return l[0] * ((N ** 2) * (l[1] - 1) + N * (l[2] - 1) + l[3])


def grid_to_cnf(cnf, N):
    f = open("temp.cnf", "w")
    cnf_bis = [[literal_to_integer(variable, N) for variable in elem] for elem in cnf]
    max_variable = abs(max(flatten(cnf_bis), key=abs))
    f.write("p cnf " + str(max_variable) + " " + str(len(cnf_bis)) + "\n")
    for elem in cnf_bis:
        f.write(" ".join(map(str, elem)) + " 0\n")
    f.close()


def flatten(l):
    return [item for sublist in l for item in sublist]


def read_grid():
    f = open(sys.argv[1], "r")
    f_read = f.read().split("\n")
    N = int(f_read[0])
    cnf = []
    for i in range(1, N + 1):
        line = list(map(int, [elem for elem in f_read[i].split(" ") if elem != '']))
        cnf.append([var(i, j + 1, line[j]) for j in range(len(line)) if line[j] != 0])
    f.close()
    return cnf, N


def get_answer(N):
    f = open("temp.txt", "r")
    f_read = f.read().split("\n")
    f.close()
    answer = []
    for elem in f_read[1][:-2].split(" "):
        if int(elem) < 0:
            continue
        answer.append(((int(elem) - 1) % N) + 1)
    return answer


def show_answer(answer, N):
    for i in range(len(answer)):
        print(answer[i], end=" ")
        if i % N == N - 1:
            print()


def resolve_cnf(N):
    os.system('minisat temp.cnf temp.txt > bin_sat.txt')
    answer = get_answer(N)
    show_answer(answer, N)
    os.system('rm temp.cnf')
    os.system('rm temp.txt')
    os.system('rm bin_sat.txt')


def resolve_grid():
    import doctest
    doctest.testmod()
    cnf, N = read_grid()
    cnf.extend(generate_rules(N))
    grid_to_cnf(cnf, N)
    resolve_cnf(N)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("not enough args")
        exit(1)
    resolve_grid()
