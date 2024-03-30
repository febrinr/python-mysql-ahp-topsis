import ahp
import connection
import time
import topsis


start_time = time.time()


cursor = connection.db.cursor()

cursor.execute("SELECT cleanliness_rating, guest_satisfaction_overall, bedrooms FROM airbnb")
decision_matrix = cursor.fetchall()

criteria_type = ['benefit', 'benefit', 'benefit']


comparison_matrix = [
    [1, 1, 3],
    [1, 1, 5],
    [1/3, 1/5, 1]
]

weight, consistency_ratio = ahp.ahp(comparison_matrix)

print("AHP Priority vector (weights):", weight)
print("AHP Consistency ratio:", consistency_ratio)

relative_closeness, rank = topsis.topsis(weight, decision_matrix, criteria_type)

# print("Number of alternatives:", len(decision_matrix))
# print("Distance:", relative_closeness)
print("Rank:", rank)

end_time = time.time()
elapsed_time = (end_time - start_time) * 1000

print("Execution time:", elapsed_time, "ms")
