import sys
import json
import operator

def recommendation(inputdata,lsh_outputdata):
    """
    recommendation algorithm
    """
    # get user data from input.json
    inputdata_list = list()
    for inputline in inputdata:
        user_data = json.loads(inputline)
        inputdata_list.append(user_data)
    inputdata = None

    # get lsh output data
    lsh_outputdata_list = list()
    for lsh_line in lsh_outputdata:
        user_pair = json.loads(lsh_line)
        lsh_outputdata_list.append(user_pair)
    lsh_outputdata = None

    recommendation_list = list()
    # get recommendation list for each user
    for user_data in inputdata_list:
        temp = list()
        candidate_movie = list()
        candidate_movie_num = list()
        # get top 5 (maybe more) most similar users for current user
        top5_similar_user_list = get_top5_similar_user(user_data, lsh_outputdata_list, inputdata_list)
        # based on the information of top 5 most similar users, get the movies they like and count for each movie
        for user_name in top5_similar_user_list:
            get_recommended_movielist(user_data[1], user_name, inputdata_list, candidate_movie, candidate_movie_num)

        # if there are more 3 users saw the movie which current user didn't see before, then recommend it
        for i in range(0, len(candidate_movie)):
            if candidate_movie_num[i] >= 3:
                temp.append(candidate_movie[i])

        # sort the recommendation movie list
        if len(temp) > 0:
            temp.sort()
            recommendation_list.append([user_data[0], temp])

    for element in recommendation_list:
        print element

def get_top5_similar_user(user_data1, lsh_outputdata, inputdata_list):
    """
    based on the current user, get him another 5 most similar users (Jaccard-based)
    """
    similar_user_list = list()
    dict = {}
    for lsh_line in lsh_outputdata:
        similar_user = ''
        if user_data1[0] == lsh_line[0]:
            similar_user = lsh_line[1]
        elif user_data1[0] == lsh_line[1]:
            similar_user = lsh_line[0]
        else:
            continue
        for user_data2 in inputdata_list:
            if similar_user == user_data2[0]:
                jaccard_value = calculate_jaccard_similarity(user_data1[1], user_data2[1])
                dict[user_data2[0]] = jaccard_value
                break

    sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))

    length = 5
    if len(sorted_dict) < 5:
        length = len(sorted_dict)
    elif len(sorted_dict) > 5:
        index = len(sorted_dict) - 5
        # if there are more than one elements having the same Jaccard Similarity as No.5's, increase the length
        while index >= 0 and sorted_dict[index-1][1] == sorted_dict[index][1]:
            index -= 1
            length += 1
    for i in range(len(sorted_dict)-1, len(sorted_dict)-1-length, -1):
        similar_user_list.append(sorted_dict[i][0])

    return similar_user_list

def calculate_jaccard_similarity(user1_movie_list, user2_movie_list):
    intersection = list(set(user1_movie_list) & set(user2_movie_list))
    union = list(set(user1_movie_list) | set(user2_movie_list))
    return float(len(intersection)) / len(union)

def get_recommended_movielist(curr_user_movie_list, user_name, inputdata_list, candidate_movie, candidate_movie_num):
    for user_data in inputdata_list:
        if user_name == user_data[0]:
            movie_list = user_data[1]
            for movie in movie_list:
                if movie in curr_user_movie_list:
                    continue
                if movie in candidate_movie:
                    i = candidate_movie.index(movie)
                    candidate_movie_num[i] += 1
                else:
                    candidate_movie.append(movie)
                    candidate_movie_num.append(1)
            break

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    lsh_outputdata = open(sys.argv[2])
    # inputdata = open('input2.json')
    # lsh_outputdata = open('Lsh_output2.json')
    recommendation(inputdata, lsh_outputdata)