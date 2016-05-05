# -*- coding: utf-8 -*-

def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """
    min_left = 100
    selected_var = None #temporary MRV variable

    #Iterate all variables 
    for var in csp.variables:
        if var.is_assigned():
            continue
        
        if len(var.domain) < min_left:
            min_left = len(var.domain)
            selected_var = var

        #Break tie by comparing number of constraints involved    
        if len(var.domain) == min_left:
            tmp_constraints = 0
            selected_constraints = 0
            for c in csp.constraints:
                if c.var1 == var or c.var2 == var:
                    tmp_constraints = tmp_constraints + 1
                if c.var1 == selected_var or c.var2 == selected_var:
                    selected_constraints = selected_constraints + 1
            if tmp_constraints > selected_constraints:
                selected_var = var
    return selected_var if selected_var else None


def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """
    #get all related constraints
    related_constraints = list()
    for c in csp.constraints:
        if c.var1 == variable or c.var2 == variable:
            related_constraints.append(c)
 
    #get all neighbors
    neighbor_vars = list()
    for c in related_constraints:
        if c.var1 == variable:
            neighbor_vars.append(c.var2)
        else:
            neighbor_vars.append(c.var1)

    #make a list of pairs which contain a value in the domain and
    #its corresponding number of related neighbor constraints
    preorder_list = list()
    for val in variable.domain:
        count = 0
        for v in neighbor_vars:
            if val in v.domain:
                count = count + 1
        tup = (val, count)
        preorder_list.append(tup)

    #sort the list based on constraint count
    preorder_list.sort(key=lambda tup: tup[1])

    #reorder domain
    for x in range (0, len(variable.domain)):
        variable.domain[x] = preorder_list[x][0]
    return variable.domain
