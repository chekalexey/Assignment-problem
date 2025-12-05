from munkres import Munkres, print_matrix
import numpy as np

matrix_size = 3
matrix = np.random.randint(0, 100, size=(matrix_size, matrix_size))
#print_matrix(matrix)

np_matrix = matrix

def MunkresAlg(np_matrix: np.matrix) -> int:
    sizes = np_matrix.shape
    if sizes[0] != sizes[1]:
        return -1
    
    m = Munkres()
    indexes = m.compute(np_matrix.tolist())
    print_matrix(np_matrix, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        value = np_matrix[row][column]
        total += value
        print(f'({row}, {column}) -> {value}')
    print(f'total cost: {total}')
    return total

final_num = MunkresAlg(np_matrix)
print(final_num)
