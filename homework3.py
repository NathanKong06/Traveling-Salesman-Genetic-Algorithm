import random
import copy
import math

def CreateRankList(population):
    """
    This function creates the rank list.
    Inputs:
        Population: List of list of paths
    Outputs:
        float: A list of tuples of index and fitness scores sorted in descending order.
    """
    rank_list = []
    for index,path in enumerate(population):
        rank_list.append((index,-CalculateEuclideanFitness(path)))
    return sorted(rank_list,key = lambda x:x[1], reverse = True)

def CalculateEuclideanFitness(path):
    """
    This function acts as a fitness function and returns the total euclidean distance of a given path.
    Inputs:
        Path: A posible path
    Outputs:
        float: Euclidean distance of given path
    """
    total_distance = 0
    for index in range(len(path) - 1):
        total_distance = total_distance + math.dist(list(map(int,path[index].split(" "))),list(map(int,path[index+1].split(" ")))) 
        #Split city in path by empty space, convert every string to ingeter by map, convert to list, calculate euclidean distance
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
    size = 1000
    cities = read_inputs()
    initial_population = CreateInitialPopulation(size,cities)
    rank_list = CreateRankList(initial_population)
    mating_pool = CreateMatingPool(initial_population,rank_list)

if __name__ == "__main__":
    main()