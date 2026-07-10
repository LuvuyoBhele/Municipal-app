import numpy as np
def priority_vector(matrix):
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_index = np.argmax(eigvals)
    max_eigvec = eigvecs[:, max_index]
    priority_vector = max_eigvec / np.sum(max_eigvec) #normalization
    return priority_vector.real

def consistency_ratio(matrix):
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_eigval = np.max(eigvals).real   # largest eigenvalue
    n = matrix.shape[0]                 # matrix size
    CI = (max_eigval - n) / (n - 1)     # consistency index
    RI = RI_dict.get(n, 1.49)           # default RI if n > 10
    CR = CI / RI if RI != 0 else 0      # consistency ratio
    return CR


#scale needs to in dictionary format with meaning attached
scale = [i for i in range(1,10)]

# Random Index values for matrices of size 1–10
RI_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
           6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}

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


        for i in range(0,len(criteria)-1):
            for j in range(0,len(criteria)-1):
                if i == j:
                    judgement_matrix[i, j] = 1
                elif i < j:
                    #find ways to improve this here so it doesn't break
                    # make sure we entering the right numbers [1/9 to 9]
                    #make the reference object clear > 1 implies refernce object is superior?
                    matrix_element_status = False
                    while matrix_element_status == False:
                        matrix_element = input(f"based on {_} how do you feel about the comparison between {criteria[i+1]} and {criteria[j+1]}? (Enter a value from 1/9 to 9): ")
                        try:
                            matrix_element = float(matrix_element)
                            if 1/9 < matrix_element < 9:
                                judgement_matrix[i, j] = matrix_element
                                judgement_matrix[j, i] = 1 / judgement_matrix[i, j]
                                matrix_element_status = True


                        except ValueError:  #will this work if i dont add a number?
                            print("Error!! \n input numerical value")
                            matrix_element_status = False


    else:
        judgement_matrix = np.zeros((len(options), len(criteria)))


        for i in range(len(options)):
            for j in range(len(criteria)):
                if i == j:
                    judgement_matrix[i, j] = 1
                elif i < j+1:
                    #make sure this process is repeated so it doesn't break
                    matrix_element_status = False
                    while matrix_element_status == False:
                        matrix_element = input(f"based on {_} how do you feel about the comparison between {options[i]} and {options[j]}? (Enter a value from 1/9 to 9): ")
                        try:
                            matrix_element = float(matrix_element)
                            if 1/9 < matrix_element < 9:
                                judgement_matrix[i, j] = matrix_element
                                judgement_matrix[j, i] = 1 / judgement_matrix[i, j]
                                matrix_element_status = True
                            else:
                                matrix_element_status == False


                        except ValueError:  #will this work if i dont add a number?
                            print("Error!! \n input numerical value")
                            matrix_element_status = False

            

                    
    #rint(judgement_matrix)

    criteria_matrix[_] = judgement_matrix

#Now we can calculate the priority vector and consistence ratio for each criterion and the overall priority vector
for _ in criteria_matrix.keys():
    pv = priority_vector(criteria_matrix[_])
    cr = consistency_ratio(criteria_matrix[_])
    criteria_matrix[_] = [criteria_matrix[_], pv, cr]

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












