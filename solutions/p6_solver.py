# -*- coding: utf-8 -*-

from collections import deque
from p1_is_complete import *
from p2_is_consistent import *
from p3_basic_backtracking import *


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P6, *you do not need to modify this method.*
    """
    return ac3(csp, csp.constraints[variable].arcs())


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P6, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None


def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns True; otherwise, it returns False.
    """

    # Base case
    if (is_complete(csp)):
        return True

    # Get first unassigned variable
    var = select_unassigned_variable(csp)

    # Iterate through domain
    for value in order_domain_values(csp, var):

        # Set rollback point
        csp.variables.begin_transaction()
        var.assign(value)

        # Inference
        if (inference(csp, var)):
            # Explore this assignment
            if is_consistent(csp, var, value):
                # GGWP
                if backtrack(csp):
                    return True
        # Nope
        csp.variables.rollback()
    return False


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())
    while queue_arcs:
        var1, var2 = queue_arcs.popleft()

        # Propagate changes in var1.domain to neighbors
        if revise(csp, var1, var2):
            if len(var1.domain) == 0:
                return False
            for (v, neighbor) in csp.constraints[var1].arcs():
                if (neighbor != var2):
                    queue_arcs.append((v, neighbor))
    return True

def revise(csp, xi, xj):

    revised = False

    # Check for consistency
    for constraint in csp.constraints[xi, xj]:

        # Check if value has non-conflicting assignments
        non_conflicts = []
        for di in xi.domain:
            non_conflicts = [dj for dj in xj.domain if constraint.is_satisfied(di, dj)]

            # This value conflicts w/ everything
            if len(non_conflicts) == 0 and di in xi.domain:
                xi.domain.remove(di)
                revised = True
    return revised