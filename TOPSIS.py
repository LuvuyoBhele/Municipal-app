#import any csv
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

#df 1
## column 1 is the alternative names
## row 1 is the criteria names


df1 = pd.read_excel("data.xlsx", sheet_name="matrix") #import the data

column_names = df1.columns.tolist() #this is a list of the names of the headers
#create a dictionary of a list where the term is a generic namea and the def is the name from excel list with the coloumn as a vector
var_col_name = {}
for i in range(1, len(column_names)):
    normalized_vector = (1/np.sqrt(np.sum(df1[column_names[i]].values**2))) * df1[column_names[i]].values 
    var_col_name[f'col_{i}'] = [column_names[i], normalized_vector * weights[i]]


#Create the matrix
matrix = np.column_stack([col[1] for col in var_col_name])

#figure out how to extract details from the next sheet and adjust 
df2 = pd.read_excel("data.xlsx", sheet_name="optimize") #import the data

optimize_direc = df2.iloc[1].tolist() 
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




#df 2
## row 1 is the criteria names
## row 2 is the optimization direction (max or min)

