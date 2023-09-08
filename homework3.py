import random
import copy
import math
import numpy as np

def FindBestAnswer(mating_pool):
    """
    Looks for the shortest path in the remaining mating pool after crossover
    Inputs:
        mating_pool: Initial mating pool
    Outputs:
        list: Best path remaining
    """
    best_distance = CalculateEuclideanFitness(mating_pool[0])
    best_path = mating_pool[0]
    for path in mating_pool:
        if CalculateEuclideanFitness(path) < best_distance:
            best_distance = CalculateEuclideanFitness(path)
            best_path = path
    return best_path

def PerformCrossOver(mating_pool):
    """
    Performs cross over and returns updated mating pool
    Inputs:
        mating_pool: Initial mating pool
    Outputs:
        list: Updated mating pool with child 
    """
    first_parent = mating_pool[0]
    second_parent = mating_pool[1]
    first_index = math.floor(len(first_parent)/3) - 1
    second_index = first_index + math.ceil(len(first_parent)/3) - 1
    child = CrossOver(first_parent,second_parent,first_index,second_index) 
    mating_pool.append(child)
    return mating_pool
    

def CheckValidPath(path, parent):
    """
    Checks and corrects path
    Inputs:
        path: Path to check
        parent: Parent to compare and fix path with
    Outputs:
        list: Same path or corrected path
    """
    count = {}
    for city in parent:
        count[city] = 1

    for path_city in path:
        count[path_city] = count[path_city] - 1

    if all(element == 0 for element in list(count.values())):
        path.append(path[0])
        return path 
    else:
        for city,value in count.items():
            if value == -1:
                repeated_city = city
                break
        for city,value in count.items():
            if value == 1:
                unused_city = city
                break
        repeated = 0
        for i in range(len(path)):
            if path[i] == repeated_city:
                repeated = repeated + 1
                if repeated == 2:
                    path[i] = unused_city
                    break
        path.append(path[0])
        return path
        
def CrossOver(parent1, parent2, start_index, end_index):
    """
    Implements a two-point crossover. Choose the subarray from parent1 starting at start_index and ending at end_index. Choose the rest of the sequence from parent2. 
    Inputs:
        parent1: First argument of the function: A list containing the random sequence of cities for the salesman to follow
        parent2: Second argument of the function: A list containing the random sequence of cities for the salesman to follow
        start_index: Start index of the SUBARRAY to be chosen from parent 1
        end_index: End index of the SUBARRAY to be chosen from parent 1
    Outputs:
        list: Return child after performing the crossover (also a list containing a valid sequence of cities)
    """
    begin_sub_array = parent2[0:start_index]
    mid_sub_array = parent1[start_index:end_index+1]
    end_sub_array = parent2[end_index+1:-1]
    sub_array = begin_sub_array + mid_sub_array + end_sub_array 
    sub_array.append(parent2[-1])
    sub_array = CheckValidPath(sub_array[:-1], parent2[:-1])
    return sub_array

def CreateOutput(path):
    """
    This function creates output.txt or overwrites if already exists with the solution.
    Inputs:
        Path: Path to be output in the file.
    Outputs:
        text file: Text file in required format of path length and path
    """
    with open ("output.txt","w") as output_file:
        output_file.write(str(CalculateEuclideanFitness(path)))
        output_file.write("\n")
        for index,city in enumerate(path):
            output_file.write(city)
            if index != len(path) - 1:
                output_file.write("\n")

def CreateRankList(population):
    """
    This function creates the rank list.
    Inputs:
        Population: List of list of paths
    Outputs:
        list: A list of tuples of index and fitness scores sorted in descending order.
    """
    rank_list = []
    for index,path in enumerate(population):
        rank_list.append((index,-CalculateEuclideanFitness(path)))
    return sorted(rank_list,key = lambda x:x[1], reverse = True)

def CalculateEuclideanFitness(path):
    """
    This function acts as a fitness function and returns the total euclidean distance of a given path (negative for fitness function)
    Inputs:
        Path: A posible path
    Outputs:
        float: Euclidean distance of given path
    """
    total_distance = 0
    for index in range(len(path) - 1):
        first_city = np.array(list(map(int,(path[index].split(" ")))))
        second_city =np.array(list(map(int,(path[index+1].split(" ")))))
        total_distance = total_distance + np.linalg.norm(first_city-second_city)
        #Split city in path by empty space, convert every string to integer by map, convert to list, calculate euclidean distance
    return total_distance

def CreateMatingPool(population, RankList):
    """
    This function defines the best fit individuals and selects them for breeding. Implements a roulette wheel-based selection which is a widely used and most efficient method for selecting parents.
    Inputs:
        Population: A list of paths from which the mating pool is to be created
        RankList: A list of tuples of index and fitness scores sorted in descending order.
    Outputs:
        list: A list of populations selected for mating (List contains paths)
    """
    mating_pool = []    
    sum = 0.0
    partial_sum = sum
    for index in range(len(RankList)):
        sum = sum + RankList[index][1]
    for _ in range(len(population)//2):
        random_num = random.uniform(sum,0.0)
        for index,tup in enumerate(RankList):
            partial_sum = partial_sum - tup[1]
            if partial_sum >= random_num:
                mating_pool.append(population[tup[0]])
                partial_sum = sum
                break
    return mating_pool

def CreateInitialPopulation(size,cities):
    """
    Creates initial populations and return them.
    Inputs:
        Size: An integer representing the size of the list (initial_population) which needs to be returned.
        Cities: A list of cities where a city is represented in 3d coordinates (x,y,z)
    Outputs:
        list: A list of paths (a permutation of cities) of size = size
    """
    initial_population = []
    permutation = copy.deepcopy(cities)
    for _ in range(int(size)):
        random.shuffle(permutation)
        permutation.append(permutation[0])
        initial_population.append(permutation)
        permutation = copy.deepcopy(cities)
    return initial_population

def read_inputs():
    """
    Reads input.txt and returns a list of all cities
    Inputs:
        N/A
    Outputs:
        list: A list of cities where a city is represented in 3d coordinates (x,y,z)
    """
    all_cities = []
    city = []
    with open("input.txt") as file:
        num_cities = file.readline()
        for _ in range(int(num_cities)):
            city = file.readline().strip()
            all_cities.append(city)
    return all_cities

def main():
    size =  10
    cities = read_inputs()
    initial_population = CreateInitialPopulation(size,cities)
    rank_list = CreateRankList(initial_population)
    mating_pool = CreateMatingPool(initial_population,rank_list)
    for _ in range(2):
        mating_pool = PerformCrossOver(mating_pool)
    best_path = FindBestAnswer(mating_pool)
    CreateOutput(best_path)
    
if __name__ == "__main__":
    main()