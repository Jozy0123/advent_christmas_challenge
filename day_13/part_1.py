from typing import Union, Optional, List
from collections import deque


def compare_element_internal(left: Union[Optional[List], Optional[int]],
                    right: Union[Optional[List], Optional[int]]):

    if left is None and right is not None:
        return True
    elif left is not None and right is None:
        return False
    elif left is None and right is None:
        return None

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None

    if isinstance(left, int) and isinstance(right, List):
        left = [left]
    elif isinstance(left, List) and isinstance(right, int):
        right = [right]

    iter_left = iter(left)
    iter_right = iter(right)

    while True:

        left_elem = next(iter_left, None)
        right_elem = next(iter_right, None)
        compare_result = compare_element_internal(left_elem, right_elem)

        if compare_result is False:
            return False
        elif compare_result is True:
            return True
        elif left_elem is None or right_elem is None:
            break


def real_iter(compare_left, compare_right):
    for i, j in zip(compare_left, compare_right):
        result = compare_element_internal(i, j)
        if result is True:
            return True
        elif result is False:
            return False

    if len(compare_left) <= len(compare_right):
        return True
    else:
        return False


def test_compare_element():
    left = [[[0, 2, [10, 5, 8]], [[], 7, [], [5, 2, 0, 1]], 6, 10], [], [[], 8, 0, 3, [4, 0, [8, 5, 8, 3]]],
     [0, [1, 5], [[8, 5, 2], 9, [8, 5, 2], [9, 9, 7, 8]], 5]]
    right = [[0, 6, [[5, 8, 6], 6, [1, 8, 2]], [[], [10], [], 3, 7], 2], [[[], 3], 7, [6, 2, []], [[]]]]
    print(real_iter(left, right))


def parse_input():
    pairs = []
    tuple_ = []
    with open("puzzle_input.txt", "r") as inputs:
        for line in inputs:
            if line != '\n':
                tuple_.append(line)
            else:
                pairs.append(tuple_)
                tuple_ = []
    return pairs


def parse_tuple(tuple_input):
    lists = []
    for i in tuple_input:
        loc = 0
        string_len = len(i)
        deque_container = deque()

        while loc < string_len:

            if i[loc] != ']' and i[loc] != ',':
                if loc + 1 < string_len:
                    if i[loc].isdigit() and i[loc+1].isdigit():
                        elem = i[loc] + i[loc + 1]
                        deque_container.appendleft(elem)
                        loc += 1
                    else:
                        deque_container.appendleft(i[loc])
                else:
                    deque_container.appendleft(i[loc])
                loc += 1
            elif i[loc] != ',':
                current_list = []
                while not len(deque_container) == 0:
                    elem = deque_container.popleft()
                    if elem != '[' and elem != ',':
                        if type(elem) is str:
                            current_list.append(int(elem))
                        else:
                            current_list.append(elem)
                    else:
                        loc += 1
                        break
                current_list.reverse()
                deque_container.appendleft(current_list)
            else:
                loc += 1
                continue
        lists.append(current_list)

    return lists

def parse_input():
    lists = []
    with open("puzzle_input.txt", "r") as inputs:
        lsts = []
        for line in inputs:
            if line != '\n':
                lsts.append(line.rstrip())
            else:
                lists.append(lsts)
                lsts = []
    return lists


if __name__ == '__main__':
    # test_compare_element()
    pairs = parse_input()
    index = 1
    sum_index = 0

    for i in pairs:
        lists = parse_tuple(i)
        for j in lists:
            print(j)
        if real_iter(*lists) is True:
            sum_index += index
            print(index)
        index += 1

    print(sum_index)





