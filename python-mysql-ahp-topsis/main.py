import ahp
import connection
import time
import topsis


start_time = time.time()


ahp.comparison_matrix = [
    [1, 1, 3],
    [1, 1, 5],
    [1/3, 1/5, 1]
]

cursor = connection.db.cursor()
cursor.execute("SELECT cleanliness_rating, guest_satisfaction_overall, bedrooms FROM airbnb")

topsis.decision_matrix = cursor.fetchall()
ahp.number_of_criteria = topsis.number_of_criteria = len(ahp.comparison_matrix)
topsis.criteria_type = ['benefit', 'benefit', 'benefit']

topsis.weight, consistency_ratio = ahp.ahp()
relative_closeness, rank = topsis.topsis()

print("AHP Priority vector (weights):", topsis.weight)
print("AHP Consistency ratio:", consistency_ratio)
# print("Distance:", relative_closeness)
print("Rank:", rank)

end_time = time.time()
elapsed_time = (end_time - start_time) * 1000

print("Execution time:", elapsed_time, "ms")
