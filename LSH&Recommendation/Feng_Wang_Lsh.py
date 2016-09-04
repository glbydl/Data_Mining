import sys
import json

"""
execute the LSH algorithm
"""
def execute_lsh(inputdata):
    similar_pair = list()
    user_signature = list()
    for line in inputdata:
        user_movie = json.loads(line)
        signature = list()
        calculate_signature(user_movie[1], signature)
        # add user identifier and his 20 min-hash signature to the user signature list
        user_signature.append([user_movie[0], signature])


    # check the current band for each user pair
    for user1 in user_signature:
        for user2 in user_signature:
            if user1[0] >= user2[0]:
                continue
            # check in each band
            for band in range(0, 5):
                # check two users' 4 values in current band are equal or not
                if (user1[1][band*4] == user2[1][band*4] and
                            user1[1][band*4+1] == user2[1][band*4+1] and
                            user1[1][band*4+2] == user2[1][band*4+2] and
                            user1[1][band*4+3] == user2[1][band*4+3]):
                    similar_pair.append([user1[0], user2[0]])
                    break

    print len(similar_pair)
    for k in similar_pair:
        print k

"""
calculate the min-hash signature
"""
def calculate_signature(movie_list, signature):
    # loop by i-th hash function
    for i in range(1, 21):
        min_index = 100
        min_signature = 100
        # loop by movie in each user's list
        for movie in movie_list:
            # calculate the new index using hash function
            new_index = (3*(movie)+i)%100
            if new_index < min_index:
                min_index = new_index
                min_signature = movie
        # add min_signature to signature list based on i-th hash function
        signature.append(min_signature)

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    # inputdata = open('input2.json')
    execute_lsh(inputdata)