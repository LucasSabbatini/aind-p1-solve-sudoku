import numpy as np 

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


# Diagonal units
def add_diagonals(boxes, unitlist):
    """
    Add diagonal units to the helping structures.

    Arg: list of boxes keys and list of the 27 standard units

    Returns: 
    - diagonal_units: list with the two possible diagonal units
    - unitlist_with_diagonals: updated unitlist with the two additional units
    - units_with_diagonals: dictionary with boxes as keys and its units as values
    - peers_with_diagonals: dictionary with boxes as keys and its peers as values
    """
    diagonal_units = [[],[]]
    for i in range(9):
        diagonal_units[0].append(row_units[i][i])
        diagonal_units[1].append(row_units[i][8-i])
    unitlist_with_diagonals = unitlist + diagonal_units

    # dictionary of 
    units_with_diagonals = dict((s, [u for u in  unitlist_with_diagonals if s in u]) for s in boxes)
    peers_with_diagonals = dict((s, set(sum(units_with_diagonals[s],[]))-set([s])) for s in boxes)

    return diagonal_units, unitlist_with_diagonals, units_with_diagonals, peers_with_diagonals

diagonal_units, unitlist_with_diagonals, units_with_diagonals, peers_with_diagonals = add_diagonals(boxes, unitlist)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


# Naked twins technique
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    

    #~No need to implement the triplets version
    # # iterating over units to find twins or triplets
    # for unit in unitlist:

    #     possible_twins_in_unit = []
    #     actual_twins_in_unit = []

    #     # iterating over box in unit and checking the values
    #     for box in unit:
    #         if len(values[box]) == 2 or len(values[box]) == 3:

    #             if values[box] in possible_twins:
    #             	actual_twins.append[values[box]]
    #             else:
    #                 possible_twins.append(values[box])

    #     # if there are twins or triplets in the unit, eliminate those values as possible for other boxes in unit.
    #     if len(actual_twins) > 0:
    #     	# iterating over found twins or triplets (probably there'll be only one per unit, if any)
    #     	for actual_twin in actual_twins:
    #     		for box in unit:
    #     			if values[box] != actual_twin:
    #     				for v in actual_twin:
    #     					if v in values[box]:
    #     						new_value = values[box].replace(v, "")
    #     						values = assign_value(values, box, new_value)


    for unit in unitlist:

        possible_twins_in_unit = []
        actual_twins_in_unit = []

        # iterating over box in unit and checking the values
        for box in unit:
            if len(values[box]) == 2:

                if values[box] in possible_twins_in_unit:
                    actual_twins_in_unit.append(values[box])
                else:
                    possible_twins_in_unit.append(values[box])

        # if there are twins in the unit, eliminate those values from possible values for other boxes in unit.
        if len(actual_twins_in_unit) > 0:
            print(actual_twins_in_unit)
            # iterating over found twins (probably there'll be only one per unit, if any)
            for actual_twin in actual_twins_in_unit:
                # going through boxes in unit that are not one of the twins.
                for box in unit:
                    if values[box] != actual_twin:
                        for v in actual_twin:
                            if v in values[box]:
                                new_value = values[box].replace(v, "")
                                values = assign_value(values, box, new_value)

    return values