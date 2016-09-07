import MapReduce
import sys
import re

"""
problem 1 social network: finding connections
"""

mr = MapReduce.MapReduce()

# mapper function
def mapper(record):
    # key: person's name
    # value: directly connected person's name
    # key and value should be exchanged for another key-value pair
    key = record[0]
    value = record[1]
    mr.emit_intermediate(key, value)
    mr.emit_intermediate(value, key)

# reducer function
def reducer(key, list_of_values):
    # key: person's name
    # value: list of directly connected people's name
    # loop for every two people in the list
    for i in range(0, len(list_of_values)):
        for j in range(i+1, len(list_of_values)):
            # sorted by people's name
            if list_of_values[i] <= list_of_values[j]:
                mr.emit((list_of_values[i], list_of_values[j], key))
            else:
                mr.emit((list_of_values[j], list_of_values[i], key))

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
