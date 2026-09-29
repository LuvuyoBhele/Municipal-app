#import any csv
## last column tells what to max and minimize
#create variables for the headers
# Create a vector from each column
# Normalize the vectors
# Multiply Each Vector with with the weights (vector scalar multilpication)
# combine the vectors into a matrix

import pandas as pd
import numpy as np
#from AHP import weights
# Load Excel file into a DataFrame

weights = [] #must automate this somehow

df = pd.read_excel("data.xlsx") #import the data

column_names = df.columns.tolist() #this is a list of the names of the headers
#create a diction of a list where the term is a generic namea and the def is the name from excel list with the coloumn as a vector
var_col_name = {}
for i in range(len(column_names)-2):
    normalized_vector = (1/np.sqrt(np.sum(df[column_names[i]].values**2))) * df[column_names[i]].values #The normalisation constant is wrong
    var_col_name[f'col_{i}'] = [column_names[i], normalized_vector * weights[i]]


#Create the matrix
matrix = np.column_stack([col[1] for col in var_col_name])

#Get another excel sheet to tell you wha to minimize or what to maximise use if statements
# i need two criteria to tell me ideal and non ideal sol
criteria = df[column_names[-1]].tolist()
ideal = df[[column_names[-2]].tolist()] #this i must review how the true or false works especially below
ideal_sol = []
non_ideal_sol = []
#go through each matrix 

while len(ideal_sol) != len(matrix) and len(non_ideal_sol) != len(matrix): #Each list must have the same number alternatives being compared
    for row in matrix:
        if criteria == 'min' and ideal == True:
            ideal_sol.append(min(row))
        elif criteria == 'max' and ideal == True:
            ideal_sol.append(max(row))
        elif criteria == 'max' and ideal == False:
            non_ideal_sol.append(max(row))
        elif criteria == 'min' and ideal == True:
            non_ideal_sol.append(min(row))


#Turn the above distances into vectors then computes the distances
def closeness(vec, ideal_vec, non_ideal_vec):
    ideal_sum = 0
    non_ideal_sum = 0
    for j in range(ideal_vec):
        ideal_sum += (vec[j] - ideal_vec[j])**2
        non_ideal_sum += (vec[j] - non_ideal_vec[j])**2

    S_neg = np.sqrt(non_ideal_sum)
    S_pos = np.sqrt(ideal_sum)
    C = S_neg/(S_neg+S_pos)

    return C





