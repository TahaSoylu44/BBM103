import os
# Custom pseudorandom number generator with a random initial seed
class PRNG:
    def __init__(self, seed=None):
        # Use a truly random seed if no seed is provided
        if seed is None:
            seed = int.from_bytes(os.urandom(4), 'big')  # Generate a random 32-bit integer
        self.state = seed

    def randint(self, low, high):
        # Simple linear congruential generator (LCG)
        self.state = (1103515245 * self.state + 12345) % (2**31)
        return low + (self.state % (high - low + 1))

# Generate logistics dataset
def generate_logistics_dataset(num_warehouses=100, max_packages=1000, seed=None):
    """Generates a logistics dataset with a random or specified seed."""
    prng = PRNG(seed)  # Initialize PRNG with the seed or a random one
    data = []
    for i in range(1, num_warehouses + 1):
        warehouse_id = f"WH-{str(i).zfill(3)}"
        priority_level = prng.randint(1, 5)
        package_count = prng.randint(0, max_packages)
        data.append([warehouse_id, priority_level, package_count])
    return data

# Save dataset to a CSV file
def save_to_csv(data, file_name):
    """Saves the dataset to a CSV file."""
    with open(file_name, "w") as file:
        # Write the header
        file.write("Warehouse_ID,Priority_Level,Package_Count\n")
        # Write each row
        for row in data:
            file.write(",".join(map(str, row)) + "\n")


######### YOUR CODE GOES HERE ---  You shoud define here two_level_sorting and the 3 sorting functions

### Your three sorting functions should have global variable named as counter. So do not return it.
def bubble_sort(dataset):
    global counter
    mylist=dataset.copy()
    result_list=[]
    number_of_elements=len(mylist)
    j=0
    while j<number_of_elements:
        for i in range(len(mylist)-1):
            if mylist[i][1]<mylist[i+1][1]:
                counter+=1
            elif mylist[i][1]==mylist[i+1][1]:
                counter+=1
                if mylist[i][-1]<=mylist[i+1][-1]:
                    continue
                else:
                    mylist[i],mylist[i+1]=mylist[i+1],mylist[i]
            else:
                mylist[i],mylist[i+1]=mylist[i+1],mylist[i]      #Swapping
                counter+=1
        result_list.append(mylist.pop())
        j+=1
    return list(reversed(result_list))

def merge_sort(mylist):
    global counter
    sorted_list=[]      #Result list
    if len(mylist)<=1:
        return mylist
    subset1=mylist[:(len(mylist)//2)]    #I am dividing my subsets until remain one single element
    subset2=mylist[(len(mylist)//2):]
    left_subset=merge_sort(subset1)
    right_subset=merge_sort(subset2)
    i=j=0
    while i<len(left_subset) and j<len(right_subset):      #While adding lists,I need to compare them.
        if left_subset[i][1]<right_subset[j][1]:
            sorted_list.append(left_subset[i])
            i+=1
        elif left_subset[i][1]==right_subset[j][1]:
            if left_subset[i][-1]<=right_subset[j][-1]:
               sorted_list.append(left_subset[i])
               i+=1 
            else:
                sorted_list.append(right_subset[j])
                j+=1
                counter+=1
        else:
            sorted_list.append(right_subset[j])
            j+=1
            counter+=1
    sorted_list.extend(left_subset[i:])          #After comparison,I need to add remaining elements.
    sorted_list.extend(right_subset[j:])
    return sorted_list


def quick_sort(mylist):
    global counter
    if len(mylist)<=1:
        return mylist
    pivot=mylist[len(mylist)//2]    
    left_list=[]     #The elements smaller than the pivot
    right_list=[]    #The elements bigger than the pivot
    middle_list=[]
    pivot_list=[]
    middle_left_list=[]
    middle_right_list=[]
    correctness=True

    for i,k in zip(mylist,mylist[1:]):
        if i[1]!=k[1]:
            correctness=False
            break

    if correctness:
        counter+=1
        for element in mylist:
            if element[-1]==pivot[-1]:
                pivot_list.append(element)
            elif element[-1]<pivot[-1]:
                middle_left_list.append(element)
            else:
                middle_right_list.append(element)
        my_middle_left_list=quick_sort(middle_left_list)
        my_middle_right_list=quick_sort(middle_right_list)
        
        return my_middle_left_list+pivot_list+my_middle_right_list
    
    else:
        for element in mylist:
            if element[1]==pivot[1]:
                middle_list.append(element)
            elif element[1]<pivot[1]:
                left_list.append(element)
            else:
                right_list.append(element)
        counter+=1

    my_left_list=quick_sort(left_list)
    my_right_list=quick_sort(right_list)
    my_middle_list=quick_sort(middle_list)
    
    return my_left_list+my_middle_list+my_right_list


def two_level_sorting(sortfunc, dataset):
    global counter
    counter = 0
    big_list = []  # List to keep all groups
    variable_list = []  # Keeps priority values already processed

    for i in dataset:
        if i[1] not in variable_list:  # If the priority value is not processed
            package_list = []  # Collects items with the same priority value
            for j in dataset:
                if j[1] == i[1]:  # Find owners with the same priority value
                    package_list.append(j)
            big_list.append(package_list.copy())  # Add group to the main list
            variable_list.append(i[1])  # Flag the Priority value

    for i in big_list.copy():           #If I have a list which has one element,it cannot be found in a list which will be used to sort package counts.
        if len(i)==1:
            big_list.remove(i)

    for i in big_list:
        sortfunc(i)
    
    sortfunc_pc_counter=counter

    counter=0

    sortfunc_sorted=sortfunc(dataset)
    
    if sortfunc==quick_sort or sortfunc==merge_sort:
        sortfunc_pl_counter=counter-sortfunc_pc_counter
    else:
        sortfunc_pl_counter=counter

    return sortfunc_sorted,sortfunc_pl_counter,sortfunc_pc_counter



#########

def write_output_file(
    bubble_sorted, merge_sorted, quick_sorted,
    bubble_sort_pl_iterations, merge_sort_pl_counter, quick_sort_pl_counter,
    bubble_sort_pc_iterations, merge_sort_pc_counter, quick_sort_pc_counter,
    merge_check, quick_check
):
    """Write sorted results and comparisons to the output file."""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as file:
        file.write("=== Bubble Sorted Results ===\n")
        # file.write(bubble_sorted.to_string() + "\n\n")
        file.write("Warehouse_ID  Priority_Level  Package_Count\n")
        file.write("-" * 40 + "\n")
        for row in bubble_sorted:
            file.write(f"{row[0]:<12}  {row[1]:<14}  {row[2]:<13}\n")
        file.write("\n")
        file.write("=== Comparison Results ===\n")
        if merge_check:
            file.write("Merge and Bubble sorts are identical.\n")
        else:
            file.write("Merge and Bubble sorts differ.\n")
        
        if quick_check:
            file.write("Quick and Bubble sorts are identical.\n")
        else:
            file.write("Quick and Bubble sorts differ.\n")
        
        file.write("\n=== Sort Performance Metrics ===\n")
        file.write(f"Bubble priority sort iteration count: {bubble_sort_pl_iterations}\n")
        file.write(f"Merge priority sort n_of right array is smaller than left: {merge_sort_pl_counter}\n")
        file.write(f"Quick priority sort recursive step count: {quick_sort_pl_counter}\n\n")
        
        file.write(f"Bubble package count sort iteration count: {bubble_sort_pc_iterations}\n")
        file.write(f"Merge package count n_of right array is smaller than left: {merge_sort_pc_counter}\n")
        file.write(f"Quick package count sort recursive step count: {quick_sort_pc_counter}\n")
    
    print(f"Results written to {OUTPUT_FILE}")
    
if __name__ == "__main__":
    # File paths and dataset size
    # Specify paths for input and output files
    INPUT_FILE = "C:\\Users\\tahas\\OneDrive\\Masaüstü\\BBM103 Assignments\\Assignment 5\\hw05_input.csv"   # Path where the generated dataset will be saved
    OUTPUT_FILE = "C:\\Users\\tahas\\OneDrive\\Masaüstü\\BBM103 Assignments\\Assignment 5\\hw05_output.txt"     # Path where the sorted results and metrics will be saved
    SIZE = 100  # Number of warehouses in the dataset

    # Generate the dataset
    dataset = generate_logistics_dataset(SIZE, max_packages=100)  # Generate a dataset with SIZE warehouses and max_packages packages
    
    # Save the generated dataset to the input file
    save_to_csv(dataset, INPUT_FILE)
    
    
    ###############################################################################################################
    # Perform sorting and counting operations
    # Sort using Bubble Sort and count iterations for Priority Level (_pl_) and Package Count (_pc_)
    bubble_sorted, bubble_sort_pl_iterations, bubble_sort_pc_iterations = two_level_sorting(bubble_sort, dataset)
    
    # Sort using Merge Sort and count recursive steps for Priority Level and Package Count
    merge_sorted, merge_sort_pl_counter, merge_sort_pc_counter = two_level_sorting(merge_sort, dataset)
    
    # Sort using Quick Sort and count recursive steps for Priority Level and Package Count
    quick_sorted, quick_sort_pl_counter, quick_sort_pc_counter = two_level_sorting(quick_sort, dataset)
    ###############################################################################################################
    
    
    # Comparisons
    # Check if Merge Sort results match Bubble Sort results
    merge_check = merge_sorted == bubble_sorted

    # Check if Quick Sort results match Bubble Sort results
    quick_check = quick_sorted == bubble_sorted

    # Write results and metrics to the output file
    write_output_file(
        bubble_sorted, merge_sorted, quick_sorted,
        bubble_sort_pl_iterations, merge_sort_pl_counter, quick_sort_pl_counter,
        bubble_sort_pc_iterations, merge_sort_pc_counter, quick_sort_pc_counter,
        merge_check, quick_check
    )


   
