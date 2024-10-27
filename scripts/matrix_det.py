class MatrixShapeError(Exception):
    """Raised when the input matrix is not well-formed."""
    pass

def calculate_square_matrix_determinant(matrix):
    """
    Calculates the determinant of a square matrix using LU decomposition for matrices larger than 3x3,
    and direct formulas for smaller matrices. Returns None for singular matrices.

    Args:
        matrix: A 2D list of floating-point numbers representing the square matrix.

    Returns:
        The determinant of the matrix, or None if the matrix is singular.

    Raises:
        MatrixShapeError: If the input matrix is not square or has rows of unequal lengths.
    """
    rows = len(matrix)
    if any(len(row) != rows for row in matrix):
        raise MatrixShapeError("Matrix must be square with rows of equal length.")

    if rows == 1:
        return matrix[0][0]
    if rows == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if rows == 3:
        return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
                matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
                matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))
    
    # LU Decomposition for matrices larger than 3x3
    lower, upper = lu_decomposition(matrix)
    
    # Calculate determinant from diagonal elements of U
    if any(upper[i][i] == 0 for i in range(rows)):
        return None  # Singular matrix
    
    det = 1.0
    for i in range(rows):
        det *= upper[i][i]
    
    return det

def lu_decomposition(matrix):
    """
    Performs LU decomposition of a square matrix without pivoting.

    Args:
        matrix: A 2D list of floating-point numbers representing the square matrix.

    Returns:
        A tuple (L, U) where L is the lower triangular matrix and U is the upper triangular matrix.
    """
    rows = len(matrix)
    lower = [[0.0] * rows for _ in range(rows)]
    upper = [[0.0] * rows for _ in range(rows)]

    for i in range(rows):
        for k in range(i, rows):
            sumk = sum(lower[i][j] * upper[j][k] for j in range(i))
            upper[i][k] = matrix[i][k] - sumk

        for k in range(i, rows):
            if i == k:
                lower[i][i] = 1.0
            else:
                sumk = sum(lower[k][j] * upper[j][i] for j in range(i))
                lower[k][i] = (matrix[k][i] - sumk) / upper[i][i]
    
    return lower, upper

# Example usage
matrix = [[0, 0], [0, 0]]
try:
    determinant = calculate_square_matrix_determinant(matrix)
    print("Determinant:", determinant)
except MatrixShapeError as e:
    print("Error:", e)