#import any csv
## last column tells what to max and minimize
#create variables for the headers
# Create a vector from each column
# Normalize the vectors
# Multiply Each Vector with with the weights (vector scalar multilpication)
# combine the vectors into a matrix

import pandas as pd
import numpy as np
# from AHP import weights
# Load Excel file into a DataFrame
# plan the data structure to be used in the app

weights = [0.4, 0.2, 0.2, 0.2] #must automate this somehow

df = pd.read_excel("data.xlsx") #import the data

column_names = df.columns.tolist() #this is a list of the names of the headers
#create a dictionary of a list where the term is a generic namea and the def is the name from excel list with the coloumn as a vector
var_col_name = {}
for i in range(len(column_names)-1):
    normalized_vector = (1/np.sqrt(np.sum(df[column_names[i]].values**2))) * df[column_names[i]].values 
    var_col_name[f'col_{i}'] = [column_names[i], normalized_vector * weights[i]]


#Create the matrix
matrix = np.column_stack([col[1] for col in var_col_name])

#the last col must tell you what to maximise or minimize this must all be for ideal case
#everything else falls into opposite
optimize_direc = df[column_names[-1]].tolist() 
ideal_sol = []
non_ideal_sol = []
#go through each matrix 

i = 0
while len(ideal_sol) != len(matrix) and len(non_ideal_sol) != len(matrix): #Each list must have the same number alternatives being compared
    while i<len(optimize_direc): #i con place this in a better way to account for error
        if optimize_direc == 'max':
            r_pos = max(matrix[i]) #find the maximum value in list
            r_neg = min(matrix[i]) #find the maximum value in list
        elif optimize_direc == 'min':
            r_neg = max(matrix[i]) #find the maximum value in list
            r_pos = min(matrix[i]) #find the maximum value in list

        ideal_sol.append(r_pos)
        non_ideal_sol.append(r_neg)
        i+=1

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





