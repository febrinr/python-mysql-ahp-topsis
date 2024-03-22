import decimal
import math
import mysql.connector
import pandas as pd
import scipy.stats as ss


def sum_comparison_matrix_rows(number_of_criteria):
    sum_matrix_columns = []

    for _ in range(number_of_criteria):
        sum_matrix_columns.append(0)

    for row in comparison_matrix:
        for index, item in enumerate(row):
            sum_matrix_columns[index] = sum_matrix_columns[index] + item

    return sum_matrix_columns


def build_normalized_matrix(number_of_criteria, sum_matrix_columns):
    normalized_matrix = []

    for row_number in range(number_of_criteria):
        normalized_row = []

        for column_number in range(number_of_criteria):
            normalized_row.append(comparison_matrix[row_number][column_number] / sum_matrix_columns[column_number])
        
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
    random_index = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
    
    return consistency_index / random_index[number_of_criteria]


def ahp(comparison_matrix):
    number_of_criteria = len(comparison_matrix)
    sum_matrix_columns = sum_comparison_matrix_rows(number_of_criteria)

    # print(sum_matrix_columns)
    # print("\n")


    normalized_matrix = build_normalized_matrix(number_of_criteria, sum_matrix_columns)

    # print(normalized_matrix)
    # print("\n")


    priority_vector = calculate_priority_vector(normalized_matrix, number_of_criteria)
    
    # print(priority_vector)
    # print("\n")


    largest_eigen_value = calculate_largest_eigen_value(number_of_criteria, priority_vector, sum_matrix_columns)
    
    # print(largest_eigen_value)
    # print("\n")
    
    
    consistency_index = calculate_consistency_index(largest_eigen_value, number_of_criteria)
    # print("CI:", consistency_index)
    # print("\n")


    consistency_ratio = calculate_consistency_ratio(consistency_index, number_of_criteria)
    # print("CR:", consistency_ratio)
    # print("\n")

    return priority_vector, consistency_ratio


comparison_matrix = [
    [1, 1, 3],
    [1, 1, 5],
    [1/3, 1/5, 1]
]

weight, consistency_ratio = ahp(comparison_matrix)

print("Priority vector:", weight)
print("Consistency ratio:", consistency_ratio)


def build_denominators_for_normalization(number_of_criteria, decision_matrix):
    sum_matrix_columns = [0] * number_of_criteria

    for alternative_scores in decision_matrix:
        for index, score in enumerate(alternative_scores):
            sum_matrix_columns[index] = sum_matrix_columns[index] + pow(score, 2)

    denominators = []

    for sum_score in sum_matrix_columns:
        denominators.append(math.sqrt(sum_score))

    return denominators


def build_weighted_normalized_matrix(number_of_criteria, decision_matrix, weight):
    denominators = build_denominators_for_normalization(number_of_criteria, decision_matrix)
    # print(denominators)
    # print("\n")

    weighted_normalized_matrix = []

    for alternative_scores in decision_matrix:
        weighted_normalized_alternative_scores = []

        for column_number in range(number_of_criteria):
            weighted_normalized_score = decimal.Decimal(weight[column_number]) * alternative_scores[column_number] / decimal.Decimal(denominators[column_number])
            weighted_normalized_alternative_scores.append(weighted_normalized_score)
        
        weighted_normalized_matrix.append(weighted_normalized_alternative_scores)

    # print(weighted_normalized_matrix)
    # print("\n")

    return weighted_normalized_matrix


def build_matrix_for_ideal_solution(number_of_criteria, weighted_normalized_matrix):
    matrix_for_ideal_solution = [[] for _ in range(number_of_criteria)]
    
    for weighted_scores in weighted_normalized_matrix:
        for index, score in enumerate(weighted_scores):
            matrix_for_ideal_solution[index].append(score)

    return matrix_for_ideal_solution


def get_ideal_solution(number_of_criteria, matrix_for_ideal_solution, criteria_type, solution_type):
    ideal_solution_matrix = [0] * number_of_criteria

    criterion_type = "benefit" if solution_type == "positive" else "cost"
    
    for index, ideal_solution_scores in enumerate(matrix_for_ideal_solution):
        if criteria_type[index] == criterion_type:
            ideal_solution_matrix[index] = max(ideal_solution_scores)
        else:
            ideal_solution_matrix[index] = min(ideal_solution_scores)
    
    return ideal_solution_matrix


def get_distance_from_positive_ideal(weighted_normalized_matrix, positive_ideal_solutions):
    distance_from_positive = []

    for weighted_scores in weighted_normalized_matrix:
        sum_distance = 0

        for index, weighted_score in enumerate(weighted_scores):
            sum_distance = sum_distance + pow(positive_ideal_solutions[index] - weighted_score, 2)

        distance = math.sqrt(sum_distance)
        
        distance_from_positive.append(distance)

    return distance_from_positive


def get_distance_from_negative_ideal(weighted_normalized_matrix, negative_ideal_solutions):
    distance_from_negative = []

    for weighted_scores in weighted_normalized_matrix:
        sum_distance = 0

        for index, weighted_score in enumerate(weighted_scores):
            sum_distance = sum_distance + pow(weighted_score - negative_ideal_solutions[index], 2)

        distance = math.sqrt(sum_distance)
        
        distance_from_negative.append(distance)

    return distance_from_negative


def get_relative_closeness_to_ideal_solution(distance_from_positive, distance_from_negative):
    relative_closeness = []

    for index, positive_distance in enumerate(distance_from_positive):
        relative_closeness.append(distance_from_negative[index] / (positive_distance + distance_from_negative[index]))
    
    return relative_closeness


def topsis(weight, decision_matrix, criteria_type):
    # print(decision_matrix)
    # print("\n")
    
    number_of_criteria = len(weight)

    weighted_normalized_matrix = build_weighted_normalized_matrix(number_of_criteria, decision_matrix, weight)

    # print(weighted_normalized_matrix)
    # print("\n")

    matrix_for_ideal_solution = build_matrix_for_ideal_solution(number_of_criteria, weighted_normalized_matrix)
    positive_ideal_solutions = get_ideal_solution(number_of_criteria, matrix_for_ideal_solution, criteria_type, "positive")
    negative_ideal_solutions = get_ideal_solution(number_of_criteria, matrix_for_ideal_solution, criteria_type, "negative")

    # print(positive_ideal_solutions)
    # print("\n")
    # print(negative_ideal_solutions)
    # print("\n")

    distance_from_positive = get_distance_from_positive_ideal(weighted_normalized_matrix, positive_ideal_solutions)

    # print(distance_from_positive)
    # print("\n")

    distance_from_negative = get_distance_from_negative_ideal(weighted_normalized_matrix, negative_ideal_solutions)

    # print(distance_from_negative)
    # print("\n")

    relative_closeness = get_relative_closeness_to_ideal_solution(distance_from_positive, distance_from_negative)
    rank = ss.rankdata(relative_closeness, "ordinal")

    data = {"Distance":relative_closeness}
    df = pd.DataFrame(data, columns=["Distance"])

    # print(relative_closeness)
    # print("\n")
    # print(rank)
    
    # return relative_closeness, rank
    return relative_closeness, rank, df['Distance'].rank(ascending=0)


db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "ahp_topsis"
)

cursor = db.cursor()

# cursor.execute("SELECT cost, quality, lead_time FROM alternatives_1")
cursor.execute("SELECT cleanliness_rating, guest_satisfaction_overall, bedrooms FROM airbnb")
decision_matrix = cursor.fetchall()

# print(decision_matrix)


# criteria = ['Cost', 'Quality', 'Lead Time']
# criteria_type = ['cost', 'benefit', 'cost']
criteria_type = ['benefit', 'benefit', 'benefit']

# decision_matrix = [
#     [1100, 5, 25],
#     [850, 3.5, 10],
#     [950, 4, 30]
# ]

relative_closeness, rank, rank_pandas = topsis(weight, decision_matrix, criteria_type)

print("Distance:", relative_closeness)
print("Rank:", rank)
print("Rank pandas:", rank_pandas)
