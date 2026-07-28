import numpy as np

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

import numpy as np

def consistency_corrector(matrix, ev, labels=None):
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
        if consistency_ratio(matrix)<0.1:
            element_update_valid = True
        else:
            element_update_valid = False

                

#scale needs to in dictionary format with meaning attached
scale = [i for i in range(1,10)]



max_options = 5
max_criteria = 5

##How many alternatives do you want to compare?

#make sure this process is repeated so it doesn't break

#- the goal here is to prevent the app from breaking when a user inputs the number of options that want they want to compare.

#-we need to make sure that input is an integer, if its not an integer we want the user to try inputing again

#-if user inputs zero then the caluclations won't work so force user to input real data


num_options_set = False
while num_options_set == False:
    num_options = input("How many options do you want to compare? (Enter a number): ")
    try:
        num_options = int(num_options)
        if num_options < 2 or num_options > max_options:
         num_options_set = False
         print(f"pick between 1 and {max_options}" )
        else:
            num_options_set = True
    
    except ValueError:  #will this work if i dont add a number?
        print("Error!! \n input numerical value")
        num_options_set = False
    
##List alternatives you want to compare?

#make sure this process is repeated so it doesn't break

#- let input be any data object (does it matter?)
#- user need to provide contextual data for analysis to be
# meaningful so if there's not data we need to ask user to input

options = [] #place holder
for i in range(num_options):
    option = None
    while option == None:
        option = input(f"Enter option {i+1}: ")
    options.append(option)

#On what criteria do you want to compare them?
#make sure this process is repeated so it doesn't break


num_criteria_set = False
while num_criteria_set == False:
    num_criteria = input("How many criteria do you want to compare? (Enter a number): ")
    try:
        num_criteria = int(num_criteria)
        if num_criteria < 2 or num_criteria > max_criteria:
         num_criteria_set = False
         print(f"pick between 1 and {max_criteria}" )
        else:
            num_criteria_set = True
    
    except ValueError:  #will this work if i dont add a number?
        print("Error!! \ninput numerical value")
        num_criteria_set = False

##List alternatives you want to compare?

#make sure this process is repeated so it doesn't break

#- let input be any data object (does it matter?)
#- user need to provide contextual data for analysis to be
# meaningful so if there's not data we need to ask user to input


criteria = ['goal',] #place holder
criteria_matrix = {}

for i in range(num_criteria):
    criterion = None
    while criterion == None:
        criterion = str(input(f"Enter criterion {i+1}: "))
        criteria.append(criterion)

#initialize the judgement matrices

for _ in criteria :
    #create judgement matrix for goal because the dimensions are defined differently to the options
    #jugdement matrix

    if _ == 'goal':
        judgement_matrix = np.zeros((len(criteria)-1, len(criteria)-1))
        #we subtracting 1 so that we don't include goal criteria


        for i in range(0,len(criteria)-1): #Represents a row index so this is what the other elements are being compared to hence this is the numerator
            for j in range(0,len(criteria)-1): #Represents a column index
                if i == j:
                    judgement_matrix[i, j] = 1
                elif i < j:
                    #find ways to improve this here so it doesn't break
                    
                    #make the reference object clear > 1 implies reference object is superior?
                    matrix_element_status = False
                    while matrix_element_status == False:
                        #choose what you feel is better
                        preference = input(f'based on {_}, what is more important {criteria[i+1]} or {criteria[j+1]}? ')
                        #check if the answer is exact
                        while preference != criteria[i+1] and preference != criteria[j+1]:
                            print('Incorrect input! \n Inputs are case sensitive so enter the exact options')
                            preference = input(f'based on {_}, what is more important {criteria[i+1]} or {criteria[j+1]}? ')
                        #Now we make the inputting of other options easy
                        if preference == criteria[i+1]:
                            not_preference = criteria[j+1]
                        else:
                            not_preference = criteria[i+1]
                            
                        #make asking the question fit the above variables
                        comparison = float(input(f'in terms of {_} how much more important is {preference} to {not_preference} ? (Enter a value from 1 to 9): '))
                        while type(comparison) != float or comparison < 1  or 9 < comparison:
                            comparison = float(input(f"Error! Input numerical value (number) between [1,9] \n in terms of {_} how much more important is {preference} to {not_preference} ? (Enter a value from 1 to 9): "))
        
                        if preference == criteria[i+1]:
                            matrix_element = comparison
                        else:
                            matrix_element =1/comparison

                        judgement_matrix[i, j] = matrix_element
                        judgement_matrix[j, i] = 1 / judgement_matrix[i, j]
                        matrix_element_status = True
                                


                        


    else:
        judgement_matrix = np.zeros((len(options), len(criteria)))


        for i in range(len(options)):
            for j in range(len(options)):
                if i == j:
                    judgement_matrix[i, j] = 1
                elif i < j+1:
                    #make sure this process is repeated so it doesn't break
                    matrix_element_status = False
                    while matrix_element_status == False:
                        #choose what you feel is better
                        preference = input(f'based on {_}, what is more important {option[i]} or {option[j]}? ')
                        #check if the answer is exact
                        while preference != option[i] and preference != option[j]:
                            print('Incorrect input! \n Inputs are case sensitive so enter the exact options')
                            preference = input(f'based on {_}, what is more important {option[i]} or {option[j]}? ')
                        #Now we make the inputting of other options easy
                        if preference == option[i]:
                            not_preference = option[j]
                        else:
                             not_preference = option[i]
                            
                        #make asking the question fit the above variables
                        comparison = float(input(f'in terms of {_} how much more important is {preference} to {not_preference} ? (Enter a value from 1 to 9): '))
                        while type(comparison) != float or comparison < 1  or 9 < comparison:
                            input(f"Error! Input numerical value (number) \n in terms of {_} how much more important is {preference} to {not_preference} ? (Enter a value from 1 to 9): ")
        
                        if preference == criteria[i+1]:
                            matrix_element = comparison
                        else:
                            matrix_element =1/comparison

                        try:
                            matrix_element = float(matrix_element)
                            if 1 < matrix_element < 9:
                                judgement_matrix[i, j] = matrix_element
                                judgement_matrix[j, i] = 1 / judgement_matrix[i, j]
                                matrix_element_status = True


                        except ValueError:  #will this work if i dont add a number?
                            print("Error!! \n input numerical value")
                            matrix_element_status = False
                        

            
    pv = priority_vector(judgement_matrix)
    cr = consistency_ratio(judgement_matrix)
    if cr > 0.1:
        print(f'inconsistency detected in {_} matrix ')
        consistency_corrector(judgement_matrix, pv, labels=options)


                    
    print(judgement_matrix)

    criteria_matrix[_] = [judgement_matrix, pv, cr]

#Now we can calculate the priority vector and consistence ratio for each criterion and the overall priority vector
#for _ in criteria_matrix.keys():
#    pv = priority_vector(criteria_matrix[_])
#    cr = consistency_ratio(criteria_matrix[_])
#    criteria_matrix[_] = [criteria_matrix[_], pv, cr]
#    if cr > 0.1:
#        print(f'inconsistency detected in {_} matrix ')

#print(criteria_matrix)

final_pv = []

for i in range(len(options)):
    row_vector = []
    for crit in criteria_matrix:
        if crit != 'goal':
            # collect option i's priority under each criterion
            row_vector.append(criteria_matrix[crit][1][i])
    # convert to NumPy array for dot product
    row_vector = np.array(row_vector)
    # dot product with normalized goal weights
    final_pv.append(np.dot(criteria_matrix['goal'][1], row_vector))

final_pv = np.array(final_pv)

# improve interpretation and output of final data
print(final_pv)


#Structure of AHP is there now your goal is to refine what you've done












