# result = []
# all edge tress
from typing import List
from copy import deepcopy


def process_arrays(arrays: List[int], init_element, is_reverse=False):
    results = []
    _max = init_element
    for i in range(1, len(arrays)-1):
        if arrays[i] > _max:
            results.append(True)
            _max = arrays[i]
        else:
            results.append(False)

    if is_reverse:
        results.reverse()

    return results

def test_process_arrays():

    arrays = [int(i) for i in '25512']
    print(process_arrays(arrays, arrays[0]))



def load_arrays():
    arrays = []
    with open("puzzle_input.txt", "r") as puzzle_input:
        for line in puzzle_input:
            line = line.rstrip()
            arrays.append([int(i) for i in line])

    return arrays

def count_trees(arrays):

    length = len(arrays)
    width = len(arrays[0])

    rows = []

    for i in range(1, length-1):
        arrays_ = deepcopy(arrays[i])
        normal = process_arrays(arrays_, arrays_[0])
        arrays_.reverse()
        reverse = process_arrays(arrays_, arrays_[0], is_reverse=True)
        new = []
        for t, j in zip(normal, reverse):
            if t is True or j is True:
                new.append(True)
            else:
                new.append(False)
        rows.append(new)

    for i in range(1, width-1):
        arrays_ = deepcopy([elem[i]for elem in arrays])
        normal = process_arrays(arrays_, arrays_[0])
        arrays_.reverse()
        reverse = process_arrays(arrays_, arrays_[0], is_reverse=True)
        new = []
        for t, j in zip(normal, reverse):
            if t is True or j is True:
                new.append(True)
            else:
                new.append(False)
        for k in range(len(new)):
            if new[k] is True:
                rows[k][i-1] = True

    return sum([sum(i)for i in rows]) + (length * 2) + (length - 2) * 2


if __name__ == "__main__":

    arrays = load_arrays()
    trees = count_trees(arrays)
    print(trees)















