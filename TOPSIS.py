import numpy as np
#Functions
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

#turn transform vectors elements in csv into floats
def Tofloat(vec):
    #for i in len(vec):
    vec = vec.replace(',', '.').astype(float).to_numpy()
    return vec


#import any csv
#create variables for the headers
# Create a vector from each column
# Normalize the vectors
# Multiply Each Vector with with the weights (vector scalar multilpication)
# combine the vectors into a matrix
#MAKE sure the csv is represents decimal places using points

import pandas as pd
import numpy as np
# from AHP import weights
# Load Excel file into a DataFrame
# plan the data structure to be used in the app

weights = [0.4, 0.2, 0.2, 0.2] #must automate this somehow

#df 1
## column 1 is the alternative names
## row 1 is the criteria names

#Import data
df1 = pd.read_csv(r"C:\Users\luvuy\Developer\Municipal app\Test_data_matrix.csv", sep=";") #import the data

#transform data
column_names = df1.columns.tolist() #this is a list of the names of the headers
#create a dictionary of a list where the term is a generic namea and the def is the name from excel list with the coloumn as a vector

#.str.replace(',', '.').astype(float). replaces the commas to decimal points then changes it to a float
#.to_numpy() changes the database column into a vector


matrix = []
var_col_name = {}
for i in range(1, len(column_names)):
    #turn all the database columns turn them into vectors
    #find the norm of the vectors
    #find the normalized vectors
    #create a dicionary of the weighted vectors
    vec = df1[column_names[i]].to_numpy()
    print(f'The vector is \n{vec}')
    norm_vec = np.linalg.norm(vec)
    print(f'normalization constant is\n{norm_vec}')
    normalized_vector = (1/norm_vec) * vec #fix this
    print(f'normalized vector is \n{normalized_vector}')
    var_col_name[i] = [column_names[i], normalized_vector * weights[i-1]]
    matrix.append(normalized_vector)

    
matrix = np.column_stack(matrix)
print(matrix)

#Create the matrix

#figure out how to extract details from the next sheet and adjust 
df2 = pd.read_csv(r"C:\Users\luvuy\Developer\Municipal app\Test_data_optimize.csv") #import the data

#how do we access the columns
optimize_direc = df2.iloc[0].tolist() 
print(len(optimize_direc))

ideal_sol = []
non_ideal_sol = []
#go through each matrix 

i = 0
while len(ideal_sol) != len(matrix[0]) and len(non_ideal_sol) != len(matrix): #Each list must have the same number alternatives being compared
    if optimize_direc[i] == 'max':
        print('ping')
        r_pos = max(matrix[i]) #find the maximum value in list
        r_neg = min(matrix[i]) #find the maximum value in list
        ideal_sol.append(r_pos)
        non_ideal_sol.append(r_neg)
    elif optimize_direc[i] == 'min':
        print('bong')
        r_neg = max(matrix[i]) #find the maximum value in list
        r_pos = min(matrix[i]) #find the maximum value in list
        ideal_sol.append(r_pos)
        non_ideal_sol.append(r_neg)
    i+=1
    if i == len(matrix[0])+1:
        break


print(f'the ideal sol: {ideal_sol}')
print(f'non_ideal_sol: {non_ideal_sol}')


#Now find the distance from the 
#take a row i from the matrix i then take one of the ideal solutions 
#subtract the vectors 
#square each element and find the sum #bascially the norm?
#take the foot

Alt_IdealSol_dist = []
Alt_nonIdealSol_dist = []

for vec in matrix:
    Sep_vec_ideal = vec - ideal_sol
    S_pos = linalg.norm(Sep_vec_ideal)
    Alt_IdealSol_dist.append(S_pos)

    Sep_vec_nonIdeal = vec - non_ideal_sol
    S_neg = linalg.norm(Sep_vec_nonIdeal)
    Alt_nonIdealSol_dist.append(S_neg)

print(len(Alt_IdealSol_dist))