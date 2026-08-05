"""
MATRIUN - Matrix utility module for TUA.

Provides functions for common matrix operations with clear,
descriptive naming throughout.
"""


def create_zero_matrix(num_rows, num_cols):
    """Return a matrix of zeros with the given dimensions."""
    return [[0] * num_cols for _ in range(num_rows)]


def create_identity_matrix(size):
    """Return a square identity matrix of the given size."""
    identity = create_zero_matrix(size, size)
    for diagonal_index in range(size):
        identity[diagonal_index][diagonal_index] = 1
    return identity


def get_matrix_dimensions(matrix):
    """Return (num_rows, num_cols) for the given matrix."""
    num_rows = len(matrix)
    num_cols = len(matrix[0]) if num_rows > 0 else 0
    return num_rows, num_cols


def add_matrices(first_matrix, second_matrix):
    """Return the element-wise sum of two matrices with identical dimensions."""
    num_rows, num_cols = get_matrix_dimensions(first_matrix)
    result_matrix = create_zero_matrix(num_rows, num_cols)
    for row_index in range(num_rows):
        for col_index in range(num_cols):
            result_matrix[row_index][col_index] = (
                first_matrix[row_index][col_index]
                + second_matrix[row_index][col_index]
            )
    return result_matrix


def multiply_matrices(left_matrix, right_matrix):
    """Return the matrix product of left_matrix and right_matrix."""
    left_rows, left_cols = get_matrix_dimensions(left_matrix)
    right_rows, right_cols = get_matrix_dimensions(right_matrix)

    if left_cols != right_rows:
        raise ValueError(
            f"Cannot multiply: left matrix has {left_cols} columns "
            f"but right matrix has {right_rows} rows."
        )

    product_matrix = create_zero_matrix(left_rows, right_cols)
    for row_index in range(left_rows):
        for col_index in range(right_cols):
            dot_product = 0
            for shared_index in range(left_cols):
                dot_product += (
                    left_matrix[row_index][shared_index]
                    * right_matrix[shared_index][col_index]
                )
            product_matrix[row_index][col_index] = dot_product
    return product_matrix


def transpose_matrix(matrix):
    """Return the transpose of the given matrix (rows become columns)."""
    num_rows, num_cols = get_matrix_dimensions(matrix)
    transposed_matrix = create_zero_matrix(num_cols, num_rows)
    for row_index in range(num_rows):
        for col_index in range(num_cols):
            transposed_matrix[col_index][row_index] = matrix[row_index][col_index]
    return transposed_matrix


def scale_matrix(matrix, scalar_factor):
    """Return a new matrix with every element multiplied by scalar_factor."""
    num_rows, num_cols = get_matrix_dimensions(matrix)
    scaled_matrix = create_zero_matrix(num_rows, num_cols)
    for row_index in range(num_rows):
        for col_index in range(num_cols):
            scaled_matrix[row_index][col_index] = (
                matrix[row_index][col_index] * scalar_factor
            )
    return scaled_matrix


def apply_wildcard_mask(matrix, wildcard_value):
    """
    Replace every element equal to wildcard_value with None.

    This resolves the wildcard handling issue: cells matching the
    wildcard are treated as unset rather than as a numeric value.
    """
    num_rows, num_cols = get_matrix_dimensions(matrix)
    masked_matrix = [row[:] for row in matrix]
    for row_index in range(num_rows):
        for col_index in range(num_cols):
            if masked_matrix[row_index][col_index] == wildcard_value:
                masked_matrix[row_index][col_index] = None
    return masked_matrix
