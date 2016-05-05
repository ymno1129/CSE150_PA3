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