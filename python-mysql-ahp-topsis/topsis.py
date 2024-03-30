import decimal
import math
import scipy.stats as ss


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

    weighted_normalized_matrix = []

    for alternative_scores in decision_matrix:
        weighted_normalized_alternative_scores = []

        for column_number in range(number_of_criteria):
            weighted_normalized_score = decimal.Decimal(weight[column_number]) * alternative_scores[column_number] / decimal.Decimal(denominators[column_number])
            weighted_normalized_alternative_scores.append(weighted_normalized_score)
        
        weighted_normalized_matrix.append(weighted_normalized_alternative_scores)

    return weighted_normalized_matrix


def build_matrix_for_ideal_solution(number_of_criteria, weighted_normalized_matrix):
    matrix_for_ideal_solution = [[] for _ in range(number_of_criteria)]
    
    for weighted_scores in weighted_normalized_matrix:
        for index, score in enumerate(weighted_scores):
            matrix_for_ideal_solution[index].append(score)

    return matrix_for_ideal_solution


def get_ideal_solution(number_of_criteria, matrix_for_ideal_solution, criteria_type):
    positive_ideal_solutions = [0] * number_of_criteria
    negative_ideal_solutions = [0] * number_of_criteria
    
    for index, ideal_solution_scores in enumerate(matrix_for_ideal_solution):
        if criteria_type[index] == "benefit":
            positive_ideal_solutions[index] = max(ideal_solution_scores)
            negative_ideal_solutions[index] = min(ideal_solution_scores)
        else:
            positive_ideal_solutions[index] = min(ideal_solution_scores)
            negative_ideal_solutions[index] = max(ideal_solution_scores)
    
    return positive_ideal_solutions, negative_ideal_solutions


def get_distance_from_ideal_solution(weighted_normalized_matrix, positive_ideal_solutions, negative_ideal_solutions):
    distance_from_positive = []
    distance_from_negative = []

    for weighted_scores in weighted_normalized_matrix:
        sum_positive_distance = 0
        sum_negative_distance = 0

        for index, weighted_score in enumerate(weighted_scores):
            sum_positive_distance += pow(positive_ideal_solutions[index] - weighted_score, 2)
            sum_negative_distance += pow(weighted_score - negative_ideal_solutions[index], 2)

        positive_distance = math.sqrt(sum_positive_distance)
        distance = math.sqrt(sum_negative_distance)
        
        distance_from_positive.append(positive_distance)
        distance_from_negative.append(distance)

    return distance_from_positive, distance_from_negative


def get_relative_closeness_to_ideal_solution(distance_from_positive, distance_from_negative):
    relative_closeness = []

    for index, positive_distance in enumerate(distance_from_positive):
        closeness = distance_from_negative[index] / (positive_distance + distance_from_negative[index])

        relative_closeness.append(closeness)
    
    return relative_closeness


def topsis(weight, decision_matrix, criteria_type):
    number_of_criteria = len(weight)

    weighted_normalized_matrix = build_weighted_normalized_matrix(
        number_of_criteria,
        decision_matrix,
        weight
    )

    matrix_for_ideal_solution = build_matrix_for_ideal_solution(
        number_of_criteria,
        weighted_normalized_matrix
    )
    
    positive_ideal_solutions, negative_ideal_solutions = get_ideal_solution(
        number_of_criteria,
        matrix_for_ideal_solution,
        criteria_type
    )

    distance_from_positive, distance_from_negative = get_distance_from_ideal_solution(
        weighted_normalized_matrix,
        positive_ideal_solutions,
        negative_ideal_solutions
    )

    relative_closeness = get_relative_closeness_to_ideal_solution(
        distance_from_positive,
        distance_from_negative
    )
    
    rank = ss.rankdata(relative_closeness, "ordinal")

    return relative_closeness, rank
