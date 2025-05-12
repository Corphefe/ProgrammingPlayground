def check_matrix(matrix):
    if matrix is None:
        raise ValueError("Given matrix cannot be None.")
    if not isinstance(matrix, list):
        raise TypeError("Given matrix must be a list of lists.")
    if not all(isinstance(row, list) for row in matrix):
        raise ValueError("Given matrix must be a list of lists.")
    n = len(matrix)
    if n == 0:
        raise ValueError("Given matrix cannot be empty.")
    if not all(len(row) == n for row in matrix):
        raise ValueError("Given matrix must be a square.")
    if not all((column > 0 for column in row) for row in matrix):
        raise ValueError("Given matrix must be a list of positive numbers.")
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("Given matrix must be symmetrical.")
    for i in range(n):
        if matrix[i][i] != 0:
            raise ValueError("Given matrix must have diagonal entries as zero.")
    return

def travelling_salesman_solution(distance_matrix):
    try:
        check_matrix(distance_matrix)
    except Exception as e:
        print(f"An error occured {e}")
        return (-1, [])
    n = len(distance_matrix)
    length_dp = []
    path_dp = []
    for _ in range((1 << (n-1))-1):
        length_row = [float('inf')] * (n - 1)
        path_row = [-1] * (n - 1)
        length_dp.append(length_row)
        path_dp.append(path_row)
    for i in range(n-1):
        length_dp[0][i] = distance_matrix[i][n-1]
        path_dp[0][i] = n-1
    for cardinality in range (1, n-1):
        for subset in range (1, (1 << (n-1))):
            if (bin(subset).count('1') == cardinality):
                for j in range(0, n-1):
                    if (1 << j) & subset == 0:
                        for l in range(0, n-1):
                            if (1 << l) & subset != 0:
                                if length_dp[subset & ~(1 << l)][l] + distance_matrix[l][j] < length_dp[subset][j]:
                                    length_dp[subset][j] = length_dp[subset & ~(1 << l)][l] + distance_matrix[l][j]
                                    path_dp[subset][j] = l
    end_city = -2
    end_subset = (1 << (n-1)) - 1
    TSP_path = [0] * (n+1)
    TSP_length = float('inf')
    for j in range(n-1):
        if (length_dp[((1 << (n-1)) - 1) & ~(1 << j)][j] + distance_matrix[j][n-1] < TSP_length):
            TSP_length = length_dp[((1 << (n-1)) - 1) & ~(1 << j)][j] + distance_matrix[j][n-1]
            end_city = j
            end_subset = ((1 << (n-1)) - 1) & ~(1 << j)
    TSP_path[0] = n-1
    TSP_path[n] = n-1
    i = 0
    while (end_city != n-1 and i < n):
        TSP_path[n - 1 - i] = end_city
        end_city = path_dp[end_subset][end_city]
        end_subset = end_subset & ~(1 << end_city)
        i += 1
    return (TSP_length, TSP_path)

TSP1 = [
    [0, 2, 9, 10],
    [2, 0, 6, 4],
    [9, 6, 0, 8],
    [10, 4, 8, 0]
]

TSP2 = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

solution1 = travelling_salesman_solution(TSP1)
solution2 = travelling_salesman_solution(TSP2)

print ("The TSP for matrix 1 is ", solution1[1], ". Which has length ", solution1[0])
print ("The TSP for matrix 2 is ", solution2[1], ". Which has length ", solution2[0])