import math
import random
from collections import Iterable
from helper.exceptions import *



def check_iterable(seq):
    if isinstance(seq, Iterable):
        return
    raise TypeError


def pick_from_list(simple_list):
    return random.choice(simple_list)


def ncr(n, r):
    f = math.factorial
    return f(n) // f(r) // f(n-r)


def median_of_tree(dict_of_three):
    if len(dict_of_three) != 3:
        raise WrongLengthException
    minimum = min(dict_of_three)
    maximum = max(dict_of_three)
    dict_of_three.pop(minimum)
    dict_of_three.pop(maximum)
    median = None
    try:
        median = list(dict_of_three.values())[0]
    except IndexError:
        raise WrongLengthException
    return median


def count_values_per_key(dict):
    counted_values_per_key= {}
    for key in dict:
        counted_values_per_key[key] = len(dict[key])
    return counted_values_per_key


def from_dict_to_set(given_dict):
    return_set = set()
    for item in given_dict:
        return_set.add(item)
        return_set.update(given_dict[item])
    return return_set

