def sum_comparison_matrix_rows(number_of_criteria, comparison_matrix):
    sum_matrix_columns = []

    for _ in range(number_of_criteria):
        sum_matrix_columns.append(0)

    for row in comparison_matrix:
        for index, item in enumerate(row):
            sum_matrix_columns[index] = sum_matrix_columns[index] + item

    return sum_matrix_columns


def build_normalized_matrix(number_of_criteria, comparison_matrix, sum_matrix_columns):
    normalized_matrix = []

    for row_number in range(number_of_criteria):
        normalized_row = []

        for column_number in range(number_of_criteria):
            normalized = comparison_matrix[row_number][column_number] / sum_matrix_columns[column_number]

            normalized_row.append(normalized)
        
        normalized_matrix.append(normalized_row)
    
    return normalized_matrix


def calculate_priority_vector(normalized_matrix, number_of_criteria):
    priority_vector = []

    for row in normalized_matrix:
        priority_vector.append(sum(row) / number_of_criteria)

    return priority_vector


def calculate_largest_eigen_value(number_of_criteria, priority_vector, sum_matrix_columns):
    multiplied = []

    for i in range(number_of_criteria):
        multiplied.append(priority_vector[i] * sum_matrix_columns[i])
    
    return sum(multiplied)


def calculate_consistency_index(largest_eigen_value, number_of_criteria):
    return (largest_eigen_value - number_of_criteria) / (number_of_criteria - 1)


def calculate_consistency_ratio(consistency_index, number_of_criteria):
    random_index = {
        1: 0.00,
        2: 0.00,
        3: 0.58,
        4: 0.90,
        5: 1.12,
        6: 1.24,
        7: 1.32,
        8: 1.41,
        9: 1.45
    }
    
    return consistency_index / random_index[number_of_criteria]


def ahp(comparison_matrix):
    number_of_criteria = len(comparison_matrix)

    sum_matrix_columns = sum_comparison_matrix_rows(
        number_of_criteria,
        comparison_matrix
    )

    normalized_matrix = build_normalized_matrix(
        number_of_criteria,
        comparison_matrix,
        sum_matrix_columns
    )
    
    priority_vector = calculate_priority_vector(
        normalized_matrix,
        number_of_criteria
    )

    largest_eigen_value = calculate_largest_eigen_value(
        number_of_criteria,
        priority_vector,
        sum_matrix_columns
    )
    
    consistency_index = calculate_consistency_index(
        largest_eigen_value,
        number_of_criteria
    )

    consistency_ratio = calculate_consistency_ratio(
        consistency_index,
        number_of_criteria
    )

    return priority_vector, consistency_ratio
