from pulp import GLPK
from pulp import LpProblem, LpVariable
from pulp.constants import LpBinary, LpMinimize, LpMaximize, LpInteger
import pandas as pd
import numpy as np
import sys
import os

# Data cleansing
filename = ""
if (len(sys.argv) != 1):
    if os.path.isfile(sys.argv[1]):
        filename = sys.argv[1]
else:
    filename = "data/PHYS-H1001-2022.csv"  ## default preference file location

preferences = pd.read_csv(filename)

if ("Timestamp" in preferences.columns):
    preferences.drop("Timestamp", axis=1, inplace=True)
elif ("Horodateur" in preferences.columns):
    preferences.drop("Horodateur", axis=1, inplace=True)

preferences["Index"] = range(preferences.index.size)
preferences.set_index("Index", inplace=True)
# Building the preferences array from the dataset
preferencesArray = np.array(preferences[preferences.columns[1:]].astype("Int64"))  # row "i" is for the "i"th student
n_students = preferencesArray.shape[0]

# Building the schedule and its maximum number of students
formatSession_df = pd.read_csv("data/physh1001-2022-formatSession.csv", index_col="Créneau")
formatSessionArray = np.array(formatSession_df["Nombre d'étudiants"].astype("Int64"))
n_slots = formatSessionArray.size
n_total_slots = formatSessionArray.sum()


# ------------------- MEET GLPK ----------------------

# Problem
problem = LpProblem("Problem", sense = LpMaximize)


# Variables
x_ij = [
    [LpVariable("x_{}_{}".format(i, j), cat=LpBinary)
     for j in range(n_slots)]
    for i in range(n_students)
]

# Constraints
# 1 : Number of students for slot j is not bigger than the max number of students allowed for slot j
for j in range(n_slots) :
    number_of_students_slot_j = 0
    for student in range(n_students) :
        number_of_students_slot_j += x_ij[student][j]

    problem += (number_of_students_slot_j <= formatSessionArray[j], "MaxStudents_{}".format(j))

# 2 A student is given exactly 1 slot
for i in range(n_students) :
    n_slots_given_for_student_i = 0
    for slot in range(n_slots) :
        n_slots_given_for_student_i += x_ij[i][slot]

    problem += (n_slots_given_for_student_i == 1, "OneSlot_{}".format(i))

# Economic function
preferences_sum = (preferencesArray.sum(axis = 1))
normalized_preferences = preferencesArray*10/ preferences_sum[:,np.newaxis]

cost = 0
for i in range(n_students) :
    for j in range(n_slots) :
        cost += x_ij[i][j]*normalized_preferences[i][j]

problem += cost, 'Objective Function'

solution = problem.solve(solver=GLPK(msg=True, keepFiles=True, timeLimit=30))



## Problem solution analysis
# matching of student ID and location in the array
student_dict = dict()
i = 0
for student in preferences["Matricule"] :
    student_dict[i] = student
    i += 1

slot_dict = dict()
i = 0
for slot in preferences.columns[1:] :
    slot_dict[i] = slot
    i += 1



schedule = preferences.copy()

for idx, row in schedule.iterrows():
    student_number = idx
    for slot in range(n_slots) :
        real_slot = slot_dict[slot]
        if(x_ij[student_number][slot].varValue == 1) :
            schedule.loc[idx,real_slot] = "X"
        else :
            schedule.loc[idx,real_slot] = " "


student_slot_dict = dict()
for i in range(n_students) :
    for j in range(n_slots) :
        if x_ij[i][j].varValue == 1 :
            student_slot_dict[student_dict[i]] = slot_dict[j]

student_slot_df = pd.DataFrame({
    "Matricule" : student_slot_dict.keys(),
    "Date": student_slot_dict.values()
})

student_slot_df.to_csv("out/Schedule_stud_and_date.csv", index = False)
schedule.to_csv("out/Schedule.csv", index = False)