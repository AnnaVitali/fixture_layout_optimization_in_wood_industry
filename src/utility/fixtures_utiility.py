SQUARE_CUP_DIM = 145
RECTANGULAR_CUP_DIM_X = 145
RECTANGULAR_CUP_DIM_Y = 55


def square_suction_cup(lb_x, lb_y):
    """
    Create a square suction cup fixture.

    Args:
        lb_x (float): The x-coordinate of the lower-left corner.
        lb_y (float): The y-coordinate of the lower-left corner.

    Returns:
        tuple: A tuple containing the x and y coordinates of the square's vertices.
    """
    square_coords = [
        (lb_x, lb_y),
        (lb_x, lb_y + SQUARE_CUP_DIM),
        (lb_x + SQUARE_CUP_DIM, lb_y + SQUARE_CUP_DIM),
        (lb_x + SQUARE_CUP_DIM, lb_y),
        (lb_x, lb_y),
    ]
    return zip(*square_coords)


def rectangle_suction_cup(lb_x, lb_y):
    """
    Create a rectangular suction cup fixture.

    Args:
        lb_x (float): The x-coordinate of the lower-left corner.
        lb_y (float): The y-coordinate of the lower-left corner.

    Returns:
        tuple: A tuple containing the x and y coordinates of the rectangle's vertices.
    """
    rectangle_coords = [
        (lb_x, lb_y),
        (lb_x, lb_y + RECTANGULAR_CUP_DIM_Y),
        (lb_x + RECTANGULAR_CUP_DIM_X, lb_y + RECTANGULAR_CUP_DIM_Y),
        (lb_x + RECTANGULAR_CUP_DIM_X, lb_y),
        (lb_x, lb_y),
    ]
    return zip(*rectangle_coords)


def create_fixture(cup_type, lb_x, lb_y):
    """
    Create a suction cup fixture based on the specified type.

    Args:
        cup_type (int): The type of suction cup (1 for square, 2 for rectangle).
        lb_x (float): The x-coordinate of the lower-left corner.
        lb_y (float): The y-coordinate of the lower-left corner.

    Returns:
        list: A list of tuples containing the x and y coordinates of the fixture's vertices.
    """
    if cup_type == 1:
        return list(square_suction_cup(lb_x, lb_y))
    elif cup_type == 2:
        return list(rectangle_suction_cup(lb_x, lb_y))
    else:
        raise ValueError("Invalid cup type: must be 1 (square) or 2 (rectangle)")
