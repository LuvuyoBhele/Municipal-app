import numpy as np
import pandas as pd
from numpy import linalg

#so now i wanna be able to change any of the ahp comparisons but also have the hint on what to change
#i also want the output of the answers to be clean



def priority_vector(matrix):
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_index = np.argmax(eigvals)
    max_eigvec = eigvecs[:, max_index]
    priority_vector = max_eigvec / np.sum(max_eigvec) #normalization
    return priority_vector.real

def consistency_ratio(matrix):
    # Random Index values for matrices of size 1–10
    RI_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_eigval = np.max(eigvals).real   # largest eigenvalue
    n = matrix.shape[0]                 # matrix size
    CI = (max_eigval - n) / (n - 1)     # consistency index
    RI = RI_dict.get(n, 1.49)           # default RI if n > 10
    CR = CI / RI if RI != 0 else 0      # consistency ratio
    return CR

def consistency_corrector(matrix, ev, labels=None):
    #when i review the options i need know what i'm pritortising
    """
    Suggests the pairwise comparison that contributes most to inconsistency
    using the eigenvalue sensitivity deviation measure.

    Parameters
    ----------
    matrix : numpy.ndarray
        Reciprocal pairwise comparison matrix.

    ev : numpy.ndarray
        Normalized right eigenvector (priority vector).

    labels : list[str], optional
        Names of the criteria/alternatives.
    """

    # Left eigenvector (eigenvector of Aᵀ)
    eigvals, eigvecs = np.linalg.eig(matrix.T)

    idx = np.argmax(eigvals.real)
    left_ev = np.real_if_close(eigvecs[:, idx])

    # Normalize left eigenvector
    left_ev = left_ev / np.sum(left_ev)

    n = matrix.shape[0]
    deviations = []

    # Compute deviation for each upper-triangular comparison
    for i in range(n):
        for j in range(i + 1, n):
            deviation = (
                left_ev[i] * ev[j]
                - (matrix[i, j] ** 2) * left_ev[j] * ev[j]
            )
            deviations.append((deviation, i, j))

    if not deviations:
        print("No comparison pairs found.")
        return matrix

    # Pair with largest deviation
    deviation, i, j = max(deviations, key=lambda x: x[0])

    left = labels[i] if labels else f"item {i+1}"
    right = labels[j] if labels else f"item {j+1}"

    print(
        f"Review comparison between '{left}' and '{right}' "
        f"(deviation = {deviation:.6f})"
    )

    while consistency_ratio(matrix) >= 0.1:
        try:
            new_value = float(
                input(f"Enter new comparison {left}/{right}: ")
            )

            if new_value <= 0:
                print("Comparison values must be positive.")
                continue

        except ValueError:
            print("Please enter a valid number.")
            continue

        matrix[i, j] = new_value
        matrix[j, i] = 1 / new_value
        print(f'new consistency ratio is :{consistency_ratio(matrix)}')

    print("Consistency ratio is now acceptable.")

    return matrix

def og_consistency_corrector(matrix, ev):

    
    trans_matrix = np.transpose(matrix)
    trans_eigvals, trans_eigvecs = np.linalg.eig(trans_matrix)
    max_trans_eigval = np.max(trans_eigvals).real
    normlized_eigvec = max_trans_eigval*(1/(np.dot(max_trans_eigval,max_trans_eigval))**1/2)
    element_deviation = {}
    #assuming ev is normalized
    for i in range(len(matrix.shape[0])): #might be wrong [rows]
        for j in range(len(matrix.shape[0])) and j > i: #might be wrong [col]
            element_deviation[matrix[i][j]] = [normlized_eigvec[i] * ev[j] - (matrix[i][j]**2) * normlized_eigvec[j] * ev[j], i, j]

    #Now the index of the biggest value in list:
    for i in range(len(element_deviation)):
        idx = element_deviation.index(max(element_deviation.values[0]))

    #Now find the element responsible in matrix list: 
    matrix_element_position = element_deviation[idx][:1]
    print(f'comparison between a and b is what must be reviewed') #
    prev_element = matrix[matrix_element_position[0],matrix_element_position[0]]
    #updated_element
    element_update_valid = False

    
    while element_update_valid == False:
        matrix[matrix_element_position[0],matrix_element_position[0]] = input("update comparison? (Enter a number): ")
        updated_element = matrix[matrix_element_position[0],matrix_element_position[0]]

        #here we must check consistency ratio until we get what we want
        validity_check = consistency_ratio(matrix)  
        if validity_check<0.1:
            element_update_valid = True
        else:
            element_update_valid = False

#scale needs to in dictionary format with meaning attached
scale = [i for i in range(1,10)]

#Import data
df1 = pd.read_csv(r"C:\Users\luvuy\Developer\Municipal app\Test_data_matrix.csv", sep=";") #import the data

#transform data
column_names = df1.columns.tolist() #this is a list of the names of the headers
#create a dictionary of a list where the term is a generic namea and the def is the name from excel list with the coloumn as a vector

#.str.replace(',', '.').astype(float). replaces the commas to decimal points then changes it to a float
#.to_numpy() changes the database column into a vector


print(f'the number of column names are: {len(column_names)} \n and the column names are \n {column_names}')



max_options = 500000
max_criteria = 500000


num_options = len(df1[column_names[0]])#input("How many options do you want to compare? (Enter a number): ")
print(f'the number of options {num_options}')


options = df1[column_names[0]].tolist() #[] #place holder  #put the options here
print(f'The options are {options}')


num_criteria =len(column_names[1:]) #input("How many criteria do you want to compare? (Enter a number): ") #put the inputs from excel file here
print(f'number of criteria: {num_criteria}')




criteria = ['goal'] + column_names[1:]#place holder

criteria_matrix = {}


judgement_matrix = np.zeros((len(criteria)-1, len(criteria)-1))
print(len(criteria)-1)

for i in range(0,len(criteria)-1): #Represents a row index so this is what the other elements are being compared to hence this is the numerator #the minus 1 is beacuse we already know one of the values in matrix
    for j in range(0,len(criteria)-1): #Represents a column index
        if i == j:
            judgement_matrix[i, j] = 1
        elif i < j:
            #find ways to improve this here so it doesn't break

            #make the reference object clear > 1 implies reference object is superior?
            matrix_element_status = False #can make check more robust by checking if the value is a float and between 1 and 9
            while matrix_element_status == False:
                    #choose what you feel is better
                preference = input(f'based on goal, what is more important {criteria[i+1]} or {criteria[j+1]}? ') #
                #check if the answer is exact
                while preference != criteria[i+1] and preference != criteria[j+1]:
                    print('Incorrect input! \n Inputs are case sensitive so enter the exact options')
                    preference = input(f'based on goal, what is more important {criteria[i+1]} or {criteria[j+1]}? ')
                #Now we make the inputting of other options easy
                #here we're making the pairwise comparison of the criteria
                if preference == criteria[i+1]:
                    not_preference = criteria[j+1]
                else:
                    not_preference = criteria[i+1]
                #make asking the question fit the above variables
                #rating of pereference
                comparison = float(input(f'in terms of goal how much more important is {preference} to {not_preference} ? (Enter a value from 1 to 9): ')) 
                while type(comparison) != float or comparison < 1  or 9 < comparison:
                    comparison = float(input(f"Error! Input numerical value (number) between [1,9] \n in terms of goal how much more important is {preference} to {not_preference} ? (Enter a value from 1 to 9): "))
                if preference == criteria[i+1]:
                    matrix_element = comparison
                else:
                    matrix_element =1/comparison
                judgement_matrix[i, j] = matrix_element
                judgement_matrix[j, i] = 1 / judgement_matrix[i, j]
                matrix_element_status = True
    print(judgement_matrix)
pv = priority_vector(judgement_matrix)
cr = consistency_ratio(judgement_matrix)#must this always be positive?
print(judgement_matrix)
if cr > 0.1:
    print(f'inconsistency detected in goal matrix ')
    consistency_corrector(judgement_matrix, pv, labels=criteria[1:]) #problem is this starts with goal and we don't care for that when we finding values to change.
print(f'the weights are: {pv}\nthe consistency ratio is {cr}') #weights we want to use

#
#
#
#
weights = pv #must automate this somehow
#
##df 1
### column 1 is the alternative names
### row 1 is the criteria names
#
#
#
#
#
matrix = []
var_col_name = {}
for i in range(1, len(column_names[1:])):
#    #turn all the database columns turn them into vectors
#    #find the norm of the vectors
#    #find the normalized vectors
#    #create a dicionary of the weighted vectors
    vec = df1[column_names[i]].to_numpy()
    print(f'The length of the vector is {len(vec)} \nthe vector is \n{vec}')
    norm_vec = np.linalg.norm(vec)
    print(f'normalization constant is\n{norm_vec}')
    normalized_vector = (1/norm_vec) * vec #fix this
    print(f'normalized vector is \n{normalized_vector}')
    var_col_name[i] = [column_names[i], normalized_vector * weights[i-1]]
    matrix.append(normalized_vector)
#
#    
matrix = np.column_stack(matrix)#1 row represents an alternative
#matrix = matrix.T
print(matrix)
#
##Create the matrix

##figure out how to extract details from the next sheet and adjust 
df2 = pd.read_csv(r"C:\Users\luvuy\Developer\Municipal app\Test_data_optimize.csv") #import the data
#
##how do we access the columns
optimize_direc = df2.iloc[0].tolist() 
print(len(optimize_direc))

ideal_sol = []
non_ideal_sol = []
#go through each matrix 
#
i = 0
while len(ideal_sol) != len(matrix[0]) and len(non_ideal_sol) != len(matrix[0]): #Each list must have the same number alternatives being compared
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

Alt_IdealSol_dist = [] #S+ distance of solutions of each option
Alt_nonIdealSol_dist = [] #S- distance of solutions of each option

for vec in matrix:
    Sep_vec_ideal = np.array(vec) - np.array(ideal_sol)
    S_pos = linalg.norm(Sep_vec_ideal)
    Alt_IdealSol_dist.append(S_pos)

    Sep_vec_nonIdeal = vec - non_ideal_sol
    S_neg = linalg.norm(Sep_vec_nonIdeal)
    Alt_nonIdealSol_dist.append(S_neg)


#I feel i can multiply by the normaliuzation constant to get the actual values

print(f"The ratings of the ideal soltion: {Alt_IdealSol_dist}") #this gives the normalised values of the ideal solution
print(f"The ratings of the non-ideal soltion: {Alt_IdealSol_dist}") #this gives the normalised values of the non ideal solution


final = {}
for i in range(len(Alt_IdealSol_dist)):
    C = Alt_nonIdealSol_dist[i]/(Alt_nonIdealSol_dist[i]+Alt_IdealSol_dist[i])
    final[options[i]]=C

final = dict(sorted(final.items(), key=lambda item: item[1], reverse=True))

print('Top 3 ideal solutions')
for rank, (option, score) in enumerate(list(final.items())[:3], start=1):
    print(f'{rank}. {option}: {score:.4f}')