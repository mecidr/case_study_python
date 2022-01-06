from math import pi, sin, cos, atan2, sqrt

dict_list = [{'name': 'business 1', 'latitude': 49.5, 'longitude': -74.2, 'reviewscore': 3.5},
             {'name': 'business 2', 'latitude': 49.1, 'longitude': -74.29, 'reviewscore': 4.5},
             {'name': 'business 3', 'latitude': 49.3, 'longitude': -74.13, 'reviewscore': 4},
             {'name': 'business 4', 'latitude': 49.5, 'longitude': -74.19},
             {'name': 'business 5', 'latitude': 50.3, 'longitude': -74.13, 'reviewscore': 4},
             {'name': 'business 6', 'latitude': 49.3, 'longitude': -74.13, 'reviewscore': 3},
             {'name': 'business 7', 'latitude': 59.3, 'longitude': -74.13, 'reviewscore': 4.8},
             {'name': 'business 8', 'latitude': 48.3, 'longitude': -74.13, 'reviewscore': 3.6},
             {'name': 'business 9', 'latitude': 49.3, 'longitude': -74.13, 'reviewscore': 4.1},
             {'name': 'business 10', 'latitude': 49.0, 'longitude': -74.12}]
# should be able to work for any point coordinate
point_coord = (49.5, -74.2)

# list of all review scores
review_scores = [element['reviewscore'] for element in dict_list if
                 'reviewscore' in element]

average_review_score = round(sum(review_scores) / len(review_scores), 1)


def calculate_distance(first_pair: tuple, second_pair: tuple):
    """ Approximates distance between in two  coordinate pairs using haversine formula """

    # I have used article mentioned below for calculating distance and converted js code shown there to python
    # Source https://www.movable-type.co.uk/scripts/latlong.html

    R = 6371e3
    phi1 = first_pair[0] * pi / 180  # latitude of first pair in radians
    phi2 = second_pair[0] * pi / 180  # latitude of second pair in radians
    delta_phi = (second_pair[0] - first_pair[0]) * pi / 180
    delta_lambda = (second_pair[1] - first_pair[1]) * pi / 180
    a = (sin(delta_phi / 2)) ** 2 + cos(phi1) * cos(phi2) * (sin(delta_lambda / 2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # distance in meters
    return round(R * c)


def get_rating(element):
    """
    returns rating based on review score and distance. If reviewscore is absent uses average review score
    """

    # +1 kilometer added to final distance in order to avoid zero division as well as getting unbeatably big rating value
    # Ex. If business is situated within 50 meters even if reviewscore is 0.1 it will get big rating value just because of distance
    # adding extra kilometer fixes it
    # those who don't have review score wil bee given average review score -0.5 ( penalty for not having reviewscore:) )
    distance = calculate_distance(point_coord, (element['latitude'], element['longitude'])) + 1000
    if 'reviewscore' in element:
        rating = element['reviewscore'] / distance
    else:
        rating = (average_review_score-0.5)/ distance
    # final rating is reversed so that closer and high review score  business will get higher rating point
    return 1 / rating


def ranker(point_coord, dict_list):
    sorted_dict_list = sorted(dict_list, key=get_rating)
    # slicing first 8 elements
    return sorted_dict_list[:8]


sorted_list = ranker(point_coord, dict_list)

# uncomment to print out the result
print(*sorted_list, sep="\n")

