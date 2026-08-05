"""Tests for the MATRIUN matrix utility module."""

import pytest
from matriun import (
    add_matrices,
    apply_wildcard_mask,
    create_identity_matrix,
    create_zero_matrix,
    get_matrix_dimensions,
    multiply_matrices,
    scale_matrix,
    transpose_matrix,
)
from matriun_cli import main as cli_main


def test_create_zero_matrix_returns_correct_dimensions():
    zero_matrix = create_zero_matrix(3, 4)
    assert len(zero_matrix) == 3
    assert all(len(row) == 4 for row in zero_matrix)


def test_create_zero_matrix_all_elements_are_zero():
    zero_matrix = create_zero_matrix(2, 3)
    assert all(element == 0 for row in zero_matrix for element in row)


def test_create_identity_matrix_has_ones_on_diagonal():
    identity = create_identity_matrix(3)
    for diagonal_index in range(3):
        assert identity[diagonal_index][diagonal_index] == 1


def test_create_identity_matrix_has_zeros_off_diagonal():
    identity = create_identity_matrix(3)
    for row_index in range(3):
        for col_index in range(3):
            if row_index != col_index:
                assert identity[row_index][col_index] == 0


def test_get_matrix_dimensions_returns_rows_and_cols():
    matrix = [[1, 2, 3], [4, 5, 6]]
    num_rows, num_cols = get_matrix_dimensions(matrix)
    assert num_rows == 2
    assert num_cols == 3


def test_get_matrix_dimensions_empty_matrix():
    num_rows, num_cols = get_matrix_dimensions([])
    assert num_rows == 0
    assert num_cols == 0


def test_add_matrices_sums_elements():
    first_matrix = [[1, 2], [3, 4]]
    second_matrix = [[5, 6], [7, 8]]
    result = add_matrices(first_matrix, second_matrix)
    assert result == [[6, 8], [10, 12]]


def test_multiply_matrices_produces_correct_product():
    left_matrix = [[1, 2], [3, 4]]
    right_matrix = [[5, 6], [7, 8]]
    result = multiply_matrices(left_matrix, right_matrix)
    assert result == [[19, 22], [43, 50]]


def test_multiply_matrices_raises_on_incompatible_dimensions():
    left_matrix = [[1, 2, 3]]
    right_matrix = [[1, 2], [3, 4]]
    with pytest.raises(ValueError, match="Cannot multiply"):
        multiply_matrices(left_matrix, right_matrix)


def test_transpose_matrix_swaps_rows_and_cols():
    matrix = [[1, 2, 3], [4, 5, 6]]
    transposed = transpose_matrix(matrix)
    assert transposed == [[1, 4], [2, 5], [3, 6]]


def test_scale_matrix_multiplies_all_elements():
    matrix = [[1, 2], [3, 4]]
    scaled = scale_matrix(matrix, scalar_factor=3)
    assert scaled == [[3, 6], [9, 12]]


def test_apply_wildcard_mask_replaces_matching_values_with_none():
    matrix = [[1, 0, 3], [0, 5, 0]]
    masked = apply_wildcard_mask(matrix, wildcard_value=0)
    assert masked == [[1, None, 3], [None, 5, None]]


def test_apply_wildcard_mask_leaves_non_matching_values_unchanged():
    matrix = [[1, 2], [3, 4]]
    masked = apply_wildcard_mask(matrix, wildcard_value=0)
    assert masked == [[1, 2], [3, 4]]


def test_apply_wildcard_mask_does_not_mutate_original_matrix():
    original = [[0, 1], [2, 0]]
    apply_wildcard_mask(original, wildcard_value=0)
    assert original == [[0, 1], [2, 0]]


def test_cli_demo_command_prints_expected_sections(capsys):
    exit_code = cli_main(["demo", "--size", "2"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "MATRIUN demo" in captured.out
    assert "Identity matrix:" in captured.out
    assert "A + B:" in captured.out


def test_cli_defaults_to_demo_when_no_command_is_given(capsys):
    exit_code = cli_main([])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "MATRIUN demo" in captured.out
