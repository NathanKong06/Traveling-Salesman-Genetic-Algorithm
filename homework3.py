import random
import copy
import math
import numpy as np

def FindAndWrite(mating_pool):
    """
    Finds best solution in mating pool and outputs to file
    Inputs:
        mating_pool: Mating pool to search through
    Outputs:
        N/A
    """
    best_path = FindBestAnswer(mating_pool)
    CreateOutput(best_path)

def MutatePath(path):
    """
    Mutates a path
    Inputs:
        path: Path to mutate
    Outputs:
        path: Mutated path
    """
    num_cities = len(path) - 1
    random_index = -1
    second_random_index = -1
    while random_index == second_random_index: #Avoid same indexes
        random_index = random.randint(1, num_cities-1) #Excluding first and last city
        second_random_index = random.randint(1, num_cities-1)
    path[random_index], path[second_random_index] = path[second_random_index], path[random_index] #Swap cities
    return path

def FindBestAnswer(mating_pool):
    """
    Looks for the shortest path in the remaining mating pool after crossover
    Inputs:
        mating_pool: Initial mating pool
    Outputs:
        list: Best path remaining
    """
    best_distance = CalculateEuclideanFitness(mating_pool[0]) #Set best_distance to the length of first path
    best_path = mating_pool[0] #Set best_path to the first path
    for path in mating_pool:
        if CalculateEuclideanFitness(path) < best_distance:
            best_distance = CalculateEuclideanFitness(path) #Find the shortest length path in the mating pool
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
    first_parent = mating_pool.pop(0) #First element in mating pool (remove)
    second_parent = mating_pool.pop(0) #Second element in mating pool (remove)
    first_index = math.floor(len(first_parent)/3) - 1 
    second_index = first_index + math.ceil(len(first_parent)/3) - 1 
    child = CrossOver(first_parent,second_parent,first_index,second_index) 
    mating_pool.append(child) #Add child to back of mating pool
    mating_pool.append(first_parent) #Re-add removed parent to back of mating pool
    mating_pool.append(second_parent) #Re-add removed parent to back of mating pool
    mutation_rate = 1/(len(mating_pool[0])-1) #Mutation rate is set to 1/number of cities
    random_chance = random.random() #Random number betwen 0 and 1
    if random_chance < mutation_rate: 
        mutated_path = MutatePath(child)
        mating_pool.append(mutated_path)
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
    count = {} #Dictionary to keep track of how many times a city has been seen
    for city in parent:
        count[city] = 1 #Initialize all cities to be seen once

    for path_city in path:
        count[path_city] = count[path_city] - 1 #Subtract 1 from all cities from the path (Repeated cities will have -1, nonused cities will be 1)

    if all(element == 0 for element in list(count.values())): #If there are no repeated cities, return the path
        path.append(path[0])
        return path 
    else: #If there are repeated cities
        repeated_cities = []
        unused_cities = []
        for city,value in count.items():
            if value == -1: #Add all repeated cities to a list
                repeated_cities.append(city)
        for city,value in count.items():
            if value == 1:
                unused_cities.append(city) #Add all unused cities to another list
        for idx,rcity in enumerate(repeated_cities):
            for index,pcity in enumerate(path):
                if rcity == pcity: #If a repeated city is found
                    path[index] = unused_cities[idx] #Replace repeated city with an unused city
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
    sub_array.append(parent2[-1]) #Re-add beginning city to have a full cycle
    sub_array = CheckValidPath(sub_array[:-1], parent2[:-1]) #Check to see if the path has no repeats
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
                output_file.write("\n") #Do not add endline element to last element

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
        rank_list.append((index,-CalculateEuclideanFitness(path))) #Negative number due to being a fitness function and needing to be in descending order (larger is better)
    return sorted(rank_list,key = lambda x:x[1], reverse = True) #Sorted by descending order based on second element in tuple (fitness score)

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
        first_city = np.array(list(map(int,(path[index].split(" "))))) #Split city in path by empty space, convert every string to integer by map, convert to list, calculate euclidean distance
        second_city = np.array(list(map(int,(path[index+1].split(" ")))))  #Basically changing ['1 2 3'] to [1,2,3]
        total_distance = total_distance + np.linalg.norm(first_city-second_city)
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
    for index in range(len(RankList)): #Calculate sum of all scores (In this case large negative number due to fitness system)
        sum = sum + RankList[index][1]
    for _ in range(len(population)//2):
        random_num = random.uniform(sum,0.0) #Random number between the sum and 0 since sum is large negative number
        for index,tup in enumerate(RankList):
            partial_sum = partial_sum - tup[1]
            if partial_sum >= random_num: #When the partial sum becomes equal to or greater than the random number, add to mating pool
                mating_pool.append(population[tup[0]])
                partial_sum = sum #Reset the partial sum
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
        permutation = copy.deepcopy(cities) #Reset permutations
    return initial_population

def CalculateNearestNeighborDistance(city1,city2):
    """
    Calculates the distance between 2 cities
    Inputs:
        city1: First city
        city2: Second city
    Outputs:
        float: Euclidean distance between 2 cities
    """
    first_city = np.array(list(map(int,(city1.split(" "))))) #Split city in path by empty space, convert every string to integer by map, convert to list, calculate euclidean distance
    second_city = np.array(list(map(int,(city2.split(" "))))) #Basically changing ['1 2 3'] to [1,2,3]
    return np.linalg.norm(first_city-second_city) 

def CreateNearestNeighborInitialPopulation(size,cities):
    """
    Creates initial populations using the nearest neighbor algorithm and return them. First finds a random city, and then finds nearest neighbors for that path.
    Inputs:
        Size: An integer representing the size of the list (initial_population) which needs to be returned.
        Cities: A list of cities where a city is represented in 3d coordinates (x,y,z)
    Outputs:
        list: A list of paths (a permutation of cities) of size = size
    """
    initial_population = []
    current_path = []
    for _ in range(int(size)):
        to_visit_indexs = set(range(len(cities))) #Indexes of cites not in the current_path (unvisited)
        current_city_index = random.choice(list(to_visit_indexs)) #Randomly select an index and "visit" it
        to_visit_indexs.remove(current_city_index) #Remove the index that has just been "visited"
        current_path.append(cities[current_city_index]) #Add to path
        while len(to_visit_indexs) > 0: #While we haven't visited every city yet
            nearest_neighbor_distance = float('inf')
            nearest_neighbor = None
            nearest_neighbor_index = -1
            for city_index in to_visit_indexs:
                current_distance = CalculateNearestNeighborDistance(cities[current_city_index],cities[city_index]) #Nearest neighbor distance
                if current_distance < nearest_neighbor_distance: #Keep track of smallest path length
                    nearest_neighbor_distance = current_distance
                    nearest_neighbor = cities[city_index]
                    nearest_neighbor_index = city_index
            current_path.append(nearest_neighbor) #Add the shortest path length between the current city and any other city ("visiting" the next city)
            to_visit_indexs.remove(nearest_neighbor_index) #Remove the city that was just visited
            current_city_index = nearest_neighbor_index #Track the index of the city that was just visited
        current_path.append(current_path[0]) #Add the starting city to the end of the path
        initial_population.append(current_path)
        current_path = [] #Reset for the next path
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

def RandomInitialPopulationMain():
    size = 25000
    cities = read_inputs()
    initial_population = CreateInitialPopulation(size,cities)
    rank_list = CreateRankList(initial_population)
    mating_pool = CreateMatingPool(initial_population,rank_list)
    for _ in range(10000):
        mating_pool = PerformCrossOver(mating_pool)
    best_path = FindBestAnswer(mating_pool)
    CreateOutput(best_path)

def main():
    size = 550
    cities = read_inputs()
    initial_population = CreateNearestNeighborInitialPopulation(size,cities)
    rank_list = CreateRankList(initial_population)
    mating_pool = CreateMatingPool(initial_population,rank_list)
    FindAndWrite(mating_pool)
    for _ in range(1000):
        mating_pool = PerformCrossOver(mating_pool)
    FindAndWrite(mating_pool)
    
if __name__ == "__main__":
    main()