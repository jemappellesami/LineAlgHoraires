import pandas as pd
from random import randint

"""
Generate random preferences file
Input : data/preferences.csv, resulting of a google forms
"""

filename = "data/preferences.csv"
preferences = pd.read_csv(filename)

default_horodat = preferences["Horodateur"][0]

#preferences.drop("Horodateur", axis=1, inplace = True)
#preferences["Index"] = range(preferences.index.size)
#preferences.set_index("Index", inplace=True)



N = 500
print(preferences.columns)
for i in range(1,N) :
    randomMatricule = randint(450000, 520000)
    index = i
    randomPreferences = [randint(1,10) for x in range(12)]
    toAppend = [default_horodat, randomMatricule] + randomPreferences
    preferences.loc[i] = toAppend

preferences.to_csv("data/RandomPreferences_{}.csv".format(N), index=False)

