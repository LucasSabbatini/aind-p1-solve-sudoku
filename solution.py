
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
def add_diagonals():
    """
    Creates diagonal units and add diagonal units to unitlist and 

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

diagonal_units, unitlist_with_diagonals, units_with_diagonals, peers_with_diagonals = add_diagonals()


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

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.


    This technique will be implemented as follows:
        1. Iterate through every possible unit
        2. Within a unit, go through every box and check if there are only two possible values
        3. Check if value has been found in other box in the same unit. If yes, it is a twin. If not, append value
           to a list of possible twins so the value will be checked when moving to next box in unit
        4. If true twins have been found, remove its values from other boxes in the same unit (non-twin boxes)

    """

    # going through every unit
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


def cross(A, B):
    """
    Cross product of elements in A and elements in B.

    Args:
        A and B: Lists to be crossed

    code source: Lesson 5 AIND
    """
    return [s+t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.

    Args:
        grid(string): A grid in string form.

    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    grid_dict = {}
    for i in range(len(grid)):
        if grid[i] == '.':
            grid_dict[boxes[i]] = '123456789'
        else:
            grid_dict[boxes[i]] = grid[i]
    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.

    Args:
        values(dict): The sudoku in dictionary form

    code source: Lesson 5 AIND
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values, diagonal=True):
    """
    Apply the elimination technique on the puzzle.

    Args:
        values(dict): The sudoku in dictionary form
        diagonal(bool): Bool defining if game is diagonal or standard
    
    Returns:
        values(dict): Resulting puzzle after applying the eliminate technique

    """


    for box in values.keys():
        if len(values[box]) == 1:
            if diagonal:
                for peer in peers_with_diagonals[box]:
                    if values[box] in values[peer]:
                        new_value = values[peer].replace(values[box], "")
                        values = assign_value(values, peer, new_value)
            else:
                for peer in peers[box]:
                    if values[box] in values[peer]:
                        new_value = values[peer].replace(values[box], "")
                        values = assign_value(values, peer, new_value)
    return values


def only_choice(values, diagonal=True):
    """
    Apply the only choice technique on the puzzle.

    Args:
        values(dict): The sudoku in dictionary form
        diagonal(bool): Bool defining if game is diagonal or standard

    Returns:
        values(dict): values(dict): Resulting puzzle after applying the only choice technique
    """

    if diagonal:
        unitlisttype = unitlist_with_diagonals
    else:
        unitlisttype = unitlist 

    for unit in unitlisttype:
        checked_values = []
        # iterating over boxes in current unit
        for box in unit:
            # only boxes with no defined values
            if len(values[box])>1:
                # iterating over values in this box
                for v in values[box]:
                    if v not in checked_values:
                        # first assume it is the only instance of this value in the unit
                        single_choice_value = True
                        # iterating over peers of box and checking if value is also them
                        for peer in unit:
                            if peer != box: 
                                if v in values[peer]:
                                    single_choice_value = False
                                    checked_values.append(v)
                    
                        if single_choice_value:
                            values = assign_value(values, box, v)
    return values


def reduce_puzzle(values, diagonal=True):
    """
    Repeatedly apply both eliminate and only_choice techniques on the puzzle, 
    till no more progress is made.
    
    Args:
        values(dict): The sudoku in dictionary form
        diagonal(bool): bool defining if game is diagonal or standard

    Returns:
        values(dict): resulting game
    or  False: bool stating there's at least one box with zero possible values

    code source: Lesson 5 AIND
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate technique
        values = eliminate(values, diagonal)
        # Only choice technique
        values = only_choice(values, diagonal)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values, diagonal=True):
    """
    Use depth first search to find a solution to the puzzle. If reduce_puzzle does not solve
    the game completely, then a value should be picked for the box with fewer remaining possible values.

    Args:
        values(dict): The sudoku in dictionary form
        diagonal(bool): bool defining if game is diagonal or standard

    Returns:
        values(dict): finished puzzle
    or  False: Bool stating the puzzle has at least one box with zero possible values.
    """

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values, diagonal)
    
    # sanity check
    if values is False:
        return False
    
    # Checking if puzzle is already complete and at the same time choosing box with fewer possible values
    solved = True
    min_len = 10
    box = ''
    for b, vs in values.items():
        if len(vs)>1:
            solved=False
            if len(vs)<min_len:
                box, min_len = b, len(vs)
    
    if solved:
        return values
   
    
    possible_values = values[box]
    for v in possible_values:
        new_puzzle = values.copy()
        new_puzzle[box] = v
        output = search(new_puzzle, diagonal)
        if output: # output may be a bool (False) or a dict with 
            return output

def solve(grid, diagonal=True):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    # transforming grid in string form to dictionary
    values = grid_values(grid)

    # soving the puzzle with the search function
    solved_puzzle = search(values, diagonal)

    return solved_puzzle



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
