import sys
import Feng_Wang_kmeans
import math

def findkstar(inputdata, threshold):
    # get the number of points in input file
    points_number = 0
    for line in inputdata:
        points_number += 1
    inputdata.seek(0)
    # corner case
    if points_number <= 2:
        return 1

    v = 1
    # get the cohesion for v
    clusters1, cohesion1 = Feng_Wang_kmeans.kmeans(inputdata, v)
    inputdata.seek(0)
    # get the cohesion for 2v
    clusters2, cohesion2 = Feng_Wang_kmeans.kmeans(inputdata, 2*v)
    inputdata.seek(0)
    # compute the normalized rate
    norm_rate = compute_norm_rate(v, 2*v, cohesion1, cohesion2)
    # keep multiplying v by 2 until the normalized rate less than the threshold
    while norm_rate >= threshold:
        v *= 2
        # if v exceeds the total number of points
        if v > points_number:
            if points_number % 2 == 0:
                v = points_number - 2
            else:
                v = points_number - 1
            break
        # get the cohesion for v
        clusters1, cohesion1 = Feng_Wang_kmeans.kmeans(inputdata, v)
        inputdata.seek(0)
        # get the cohesion for 2v
        clusters2, cohesion2 = Feng_Wang_kmeans.kmeans(inputdata, 2*v)
        inputdata.seek(0)
        # compute the normalized rate
        norm_rate = compute_norm_rate(v, 2*v, cohesion1, cohesion2)

    # get the k* by executing binary search
    kstar = binary_search(v/2, v, inputdata, threshold)
    return kstar

# find k* by binary search on [v/2, v]
def binary_search(left, right, inputdata, threshold):
    # if the range is equal to or less than 1, return the boundary with higher cohesion
    if right - left <= 1:
        c1, co1 = Feng_Wang_kmeans.kmeans(inputdata, left)
        inputdata.seek(0)
        c2, co2 = Feng_Wang_kmeans.kmeans(inputdata, right)
        inputdata.seek(0)
        if co1 < co2:
            return left
        else:
            return right
    mid = (left + right) / 2
    # get the cohesion for mid
    clusters_mid, cohesion_mid = Feng_Wang_kmeans.kmeans(inputdata, mid)
    inputdata.seek(0)
    # get the cohesion for right
    clusters_right, cohesion_right = Feng_Wang_kmeans.kmeans(inputdata, right)
    inputdata.seek(0)
    # compute the normalized rate
    norm_rate = compute_norm_rate(mid, right, cohesion_mid, cohesion_right)
    # if normalized rate is less than threshold, search on [left, mid], otherwise search on [mid, right]
    if norm_rate < threshold:
        return binary_search(left, mid, inputdata, threshold)
    else:
        return binary_search(mid, right, inputdata, threshold)

# compute the normalized rate
def compute_norm_rate(left, right, cohesion1, cohesion2):
    numerator = math.fabs(cohesion1 - cohesion2)
    denominator = cohesion1 * (right - left)
    return float(numerator) / denominator

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    threshold = float(sys.argv[2])
    kstar = findkstar(inputdata, threshold)
    print kstar