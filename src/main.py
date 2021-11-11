from pulp import GLPK
from pulp import LpProblem, LpVariable
from pulp.constants import LpBinary, LpMinimize, LpMaximize, LpInteger
import pandas as pd
import numpy as np
import sys
import os
from random import randint

# Nettoyage des données
filename = ""
if (len(sys.argv) != 1) :
    if os.path.isfile(sys.argv[1]):
        filename = sys.argv[1]
else :
    filename = "data/preferences.csv"   ## default preference file location

preferences = pd.read_csv(filename)

preferences.drop("Horodateur", axis=1, inplace = True)
preferences["Index"] = range(preferences.index.size)
preferences.set_index("Index", inplace=True)
# preferences["Matricule"].apply(lambda x : str(x).split("000")[-1])

# Brouillon : ajout d'un nombre N d'étudiants dans le fichier de préférences, génération aléatoire !
N = 50
print(preferences.columns)
for i in range(1,N) :
    randomMatricule = randint(450000, 520000)
    index = i
    randomPreferences = [randint(1,10) for x in range(12)]
    toAppend = [randomMatricule] + randomPreferences
    preferences.loc[i] = toAppend

preferences.to_csv("data/RandomPreferences.csv")

