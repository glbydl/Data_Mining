import MapReduce
import sys
import re

"""
problem2 desciptive statistics: variance
"""

mr = MapReduce.MapReduce()

# mapper function
def mapper(record):
    # key: 1
    # value: original data and square of the data pair
    key = 1
    for data in record:
        value = (data, data**2)
        mr.emit_intermediate(key, value)

# reducer function
def reducer(key, list_of_values):
    
    size = len(list_of_values)
    data_sum = 0
    square_sum = 0

    # key: 1
    # value: the list of original data and square of the data pair
    for array in list_of_values:
        data_sum += array[0]
        square_sum += array[1]

    result = float(square_sum)/size - (float(data_sum)/size)**2
    mr.emit(result)

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
    
