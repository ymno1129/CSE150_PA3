# -*- coding: utf-8 -*-

from collections import deque


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
        # for variable in csp.variables:
        #     print variable, variable.domain

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
    for di in xi.domain:
        for dj in xj.domain:
            # Remove conflicting values from domain
            for constraint in csp.constraints[xi, xj]:
                if not constraint.is_satisfied(di, dj) and di in xi.domain:
                    xi.domain.remove(di)
                    revised = True
    return revised