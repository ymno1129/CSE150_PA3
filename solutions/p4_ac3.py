# -*- coding: utf-8 -*-

from collections import deque


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""

    #I'm not sure if this is correct

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())
    while queue_arcs:
        arc = queue_arcs.pop()
        var1 = arc[0]
        var2 = arc[1]
        if var1.is_assigned() and var2.is_assigned():
            if var1.value == var2.value:
                return False

        if var1.is_assigned():
            dom = var2.domain
            for val in dom:
                if val == var1.value:
                    return False

        if var2.is_assigned():
            dom = var1.domain
            for val in dom:
                if val == var2.value:
                    return False
    return True

    # TODO implement this
    pass

def revise(csp, xi, xj):
    # You may additionally want to implement the 'revise' method.
    pass
