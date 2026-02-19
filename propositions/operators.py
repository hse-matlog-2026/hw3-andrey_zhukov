# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2022
# File name: propositions/operators.py

"""Syntactic conversion of propositional formulas to use only specific sets of
operators."""

from propositions.syntax import *
from propositions.semantics import *

def to_not_and_or(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'``, ``'&'``, and ``'|'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'``, ``'&'``, and
        ``'|'``.
    """
    # Task 3.5
    if formula.root == 'T':
        return Formula.parse('(p|~p)')
    if formula.root == 'F':
        return Formula.parse('~(p|~p)')

    if formula.first is None and formula.second is None:
        return formula

    if formula.root == '~':
        return Formula('~', to_not_and_or(formula.first))

    left = to_not_and_or(formula.first)
    right = to_not_and_or(formula.second)

    if formula.root == '&':
        return Formula('&', left, right)

    if formula.root == '|':
        return Formula('|', left, right)

    if formula.root == '->':
        return Formula.parse('(~p|q)').substitute_variables({'p': left, 'q': right})

    if formula.root == '+':
        return Formula.parse('~((p&q)|(~p&~q))').substitute_variables({'p': left, 'q': right})

    if formula.root == '<->':
        return Formula.parse('((p&q)|(~p&~q))').substitute_variables({'p': left, 'q': right})

    if formula.root == '-&':
        return Formula.parse('~(p&q)').substitute_variables({'p': left, 'q': right})

    if formula.root == '-|':
        return Formula.parse('~(p|q)').substitute_variables({'p': left, 'q': right})

def to_not_and(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'`` and ``'&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'`` and ``'&'``.
    """
    # Task 3.6a
    f = to_not_and_or(formula)

    if f.first is None and f.second is None:
        return f

    if f.root == '~':
        return Formula('~', to_not_and(f.first))

    left = to_not_and(f.first)
    right = to_not_and(f.second)

    if f.root == '&':
        return Formula('&', left, right)

    if f.root == '|':
        return Formula.parse('~(~p&~q)').substitute_variables({'p': left, 'q': right})

def to_nand(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'-&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'-&'``.
    """
    # Task 3.6b
    f = to_not_and(formula)

    if f.first is None and f.second is None:
        return f

    if f.root == '~':
        inner = to_nand(f.first)
        return Formula('-&', inner, inner)

    left = to_nand(f.first)
    right = to_nand(f.second)

    if f.root == '&':
        temp = Formula('-&', left, right)
        return Formula('-&', temp, temp)

def to_implies_not(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'~'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'~'``.
    """
    # Task 3.6c
    f = to_not_and_or(formula)

    if f.first is None and f.second is None:
        return f

    if f.root == '~':
        return Formula('~', to_implies_not(f.first))

    left = to_implies_not(f.first)
    right = to_implies_not(f.second)

    if f.root == '&':
        return Formula.parse('~(p->~q)').substitute_variables({'p': left, 'q': right})

    if f.root == '|':
        return Formula.parse('(~p->q)').substitute_variables({'p': left, 'q': right})

def to_implies_false(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'F'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'F'``.
    """
    # Task 3.6d
    f = to_implies_not(formula)

    # Переменная или F
    if f.first is None and f.second is None:
        return f

    if f.root == '~':
        inner = to_implies_false(f.first)
        return Formula('->', inner, Formula('F'))

    left = to_implies_false(f.first)
    right = to_implies_false(f.second)

    if f.root == '->':
        return Formula('->', left, right)
