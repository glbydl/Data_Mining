import sys
import json
import math

def kmeans(inputdata, k):
    """
    k-means algorithm
    :param inputdata: points coordinates info
    :param k: the k value
    :return: clusterings and cohesion
    """
    clusterings = list()
    cohesion = 0
    # coordinates list of points
    coordinates = list()
    # dictionary containing distance between two points
    # dict.get(i).get(j) denotes the distance between point i and point j
    # i and j are the line number which points belong to, starting from 0
    dict = {}
    # clustering list
    clusters = list()
    # centroid list of clusterings
    centroid_list = list()
    # backup of centroid list
    centroid_list_bk = list()
    # cluster containing all points
    whole_cluster = list()
    count = 0
    for line in inputdata:
        coordinate = json.loads(line)
        coordinates.append(coordinate)
        whole_cluster.append(count)
        count += 1

    dimension = 0
    if (len(coordinates) > 0):
        dimension = len(coordinates[0])

    # set up dict
    for i in range(0, len(coordinates)):
        dict[i] = {}
        for j in range(0, len(coordinates)):
            if (i != j):
                tmp = dict.get(i)
                tmp[j] = calculate_distance(coordinates[i], coordinates[j])

    # main functionality
    if k == 1:
        # when k == 1, there is only one cluster, all points belong to it.
        result = list()
        for coordinate in coordinates:
            temp_coordinate = list(coordinate)
            result.append(tuple(temp_coordinate))
        sort_by_coordinate(result)
        return [result], compute_cohesion(whole_cluster, dict)
    else:
        # add the first point as the first cluster
        clusters.append([0])
        # initialize clusters list
        for i in range(0, k-1):
            get_point_index(dict, clusters)

        for cluster in clusters:
            centroid_list.append(coordinates[cluster[0]])

        # re-compute the clusters until it gets stablized
        while centroid_list != centroid_list_bk:
            centroid_list_bk = list(centroid_list)
            compute_clusters(dict, clusters, coordinates, centroid_list)
            update_centroid_list(clusters, centroid_list, coordinates, dimension)

        for i in range(0, len(clusters)):
            result = list()
            # set the result for cluster i
            for point_index in clusters[i]:
                result.append(coordinates[point_index])
            # sort the result cluster by coordinates
            sort_by_coordinate(result)
            # sum the cohesion
            cohesion += compute_cohesion(clusters[i], dict)
            clusterings.append(result)

        # get the average cohesion
        cohesion /= k

    return clusterings, cohesion

# compute the cohesion. cohesion = avg of diameters of all clusters
def compute_cohesion(cluster, dict):
    max_diameter = 0
    for i in range(0, len(cluster)-1):
        for j in range(i+1, len(cluster)):
            if dict.get(cluster[i]).get(cluster[j]) > max_diameter:
                max_diameter = dict.get(cluster[i]).get(cluster[j])
    return math.sqrt(max_diameter)

def compute_clusters(dict, clusters, coordinates, centroid_list):
    for key in dict:
        min_distance = sys.maxint
        min_distance_index = -1

        # delete the key from the cluster containing it
        for cluster in clusters:
            if key in cluster:
                cluster.remove(key)

        for i in range(0, len(clusters)):
            distance = calculate_distance(coordinates[key], centroid_list[i])

            if distance < min_distance:
                min_distance = distance
                min_distance_index = i

        clusters[min_distance_index].append(key)

# update centroid list
def update_centroid_list(clusters, centroid_list, coordinates, dimension):
    for i in range(0, len(clusters)):
        centroid_list[i] = compute_centroid(clusters[i], coordinates, dimension)

def isExist(key, clusters):
    for cluster in clusters:
        if key == cluster[0]:
            return True
    return False

# compute the centroid for the current cluster
def compute_centroid(cluster, coordinates, dimension):
    size = len(cluster)
    centroid = list()
    for i in range(0, dimension):
        centroid.append(0)
    for index in cluster:
        for j in range(0, dimension):
            centroid[j] += coordinates[index][j]
    for i in range(0, dimension):
        centroid[i] = float (centroid[i]) / size
    return centroid

# get point indices for the initial k
def get_point_index(dict, clusters):
    max_distance = 0
    max_distance_key = -1
    for key in dict:
        if isExist(key, clusters):
            continue
        distance_dict = dict.get(key)
        distance = sys.maxint
        for i in range(0, len(clusters)):
            temp = math.sqrt(distance_dict.get(clusters[i][0]))
            if temp < distance:
                distance = temp
        if distance > max_distance:
            max_distance = distance
            max_distance_key = key
    clusters.append([max_distance_key])

"""
def get_point_index(dict, clusters):
    max_distance = 0
    max_distance_key = -1
    for key in dict:
        distance_dict = dict.get(key)
        distance = 0
        if isExist(key, clusters):
            continue

        for i in range(0, len(clusters)):
            distance += math.sqrt(distance_dict.get(clusters[i][0]))
        if distance > max_distance:
            max_distance = distance
            max_distance_key = key
    clusters.append([max_distance_key])
"""

# computer the distance(square) between two points
def calculate_distance(coordinate1, coordinate2):
    squaresum = 0.0
    for i in range(0, len(coordinate1)):
        squaresum += (coordinate1[i] - coordinate2[i])**2
    return squaresum

def sort_by_coordinate(cluster):
    for i in range(0, len(cluster)-1):
        for j in range(i+1, len(cluster)):
            if isGreaterThan(cluster[i], cluster[j]):
                temp = cluster[i]
                cluster[i] = cluster[j]
                cluster[j] = temp

def isGreaterThan(point1, point2):
    for i in range(0, len(point1)):
        if point1[i] > point2[i]:
            return True
        elif point1[i] < point2[i]:
            return False
    return False

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    k = int(sys.argv[2])
    # execute the kmeans algorithm
    clusters, cohesion = kmeans(inputdata, k)
    # print out the result
    for cluster in clusters:
        print cluster
    print cohesion