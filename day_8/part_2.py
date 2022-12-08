# result = []
# all edge tress

from typing import List
from copy import deepcopy


def process_arrays(arrays: List[int], is_reverse=False):
    results = []

    for i in range(1, len(arrays)-1):
        count = 0
        for j in range(i-1, -1, -1):
            if arrays[i] > arrays[j]:
                count += 1
            else:
                count += 1
                break
        results.append(count)

    if is_reverse:
        results.reverse()

    return results

def test_process_arrays():

    arrays = [int(i) for i in '23512']
    print(process_arrays(arrays))



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
        normal = process_arrays(arrays_)
        arrays_.reverse()
        reverse = process_arrays(arrays_, is_reverse=True)
        new = []
        for t, j in zip(normal, reverse):
            new.append(t*j)
        rows.append(new)

    for i in range(1, width-1):
        arrays_ = deepcopy([elem[i]for elem in arrays])
        normal = process_arrays(arrays_)
        arrays_.reverse()
        reverse = process_arrays(arrays_, is_reverse=True)
        new = []
        for t, j in zip(normal, reverse):
            new.append(t*j)
        for k in range(len(new)):
            rows[k][i-1] *= new[k]

    return max([max(i) for i in rows])


if __name__ == "__main__":

    arrays = load_arrays()
    test_process_arrays()
    trees = count_trees(arrays)
    print(trees)
