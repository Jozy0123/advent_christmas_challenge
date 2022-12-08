from functools import lru_cache
from typing import Optional, List

class DirectoryTreeNode:

    def __init__(self,
                 parent_folder_node=None,
                 folder_or_filename=None,
                 is_file: bool = False,
                 file_size: int = 0):
        self.folder_or_filename = folder_or_filename
        self.child_folders_nodes = []
        self.parent_folder_node = parent_folder_node
        self.is_file = is_file
        if is_file:
            self.file_size = file_size

    def add_child_dir(self, child_folder_node):
        self.child_folders_nodes.append(child_folder_node)

    def go_to_child_node(self, child_folder_name):
        for i in self.child_folders_nodes:
            if i.folder_or_filename == child_folder_name:
                return i

    def get_parent_folder_node(self):
        return self.parent_folder_node

    @property
    @lru_cache(maxsize=2000)
    def get_size(self):
        size = 0
        if self.is_file:
            size = self.file_size
        else:
            for i in self.child_folders_nodes:
                size += i.get_size

        return size

    def traverse_size(self):
        for child in self.child_folders_nodes:
            if not child.is_file:
                yield from child.traverse_size()
        if not self.is_file:
            yield self.get_size

    def __repr__(self):
        return f"{self.folder_or_filename}"

    def print_tree(self):
        for child in self.child_folders_nodes:
            child.print_tree()
        print(self.folder_or_filename)


def test_trees():
    root_node = DirectoryTreeNode(None, "/")
    child_node = DirectoryTreeNode(root_node, "abc")
    root_node.add_child_dir(child_node)
    child_node_2 = DirectoryTreeNode(root_node, "cde")
    root_node.add_child_dir(child_node_2)
    child_node_3 = DirectoryTreeNode(root_node,
                                     'file.txt',
                                     is_file=True,
                                     file_size=23)
    child_node_2.add_child_dir(child_node_3)
    root_node.print_tree()

    iter_ = root_node.traverse_size()
    for i in iter_:
        print(i)


def parse_line(line: str):
    parsed_tuple = [None, None, None]
    elements = line.rstrip().split(" ")
    if elements[0] == '$':
        parsed_tuple[0] = "command"
        if elements[1] == 'ls':
            parsed_tuple[1] = 'get_child_node_and_file'
        else:
            parsed_tuple[1] = 'go_to_child_node'
            parsed_tuple[2] = elements[2]

    elif elements[0] == "dir":
        parsed_tuple[0] = 'child_node'
        parsed_tuple[1] = elements[1]
    else:
        parsed_tuple[0] = 'file'
        parsed_tuple[1] = elements[1]
        parsed_tuple[2] = int(elements[0])

    return parsed_tuple


def get_size_of_folders():
    cur_node = tree_root = DirectoryTreeNode(parent_folder_node=None,
                                             folder_or_filename="/")
    with open("puzzle_input.txt", "r") as puzzle:
        for line in puzzle:
            parsed_tuple = parse_line(line)
            if parsed_tuple[0] == 'file':
                child_node = DirectoryTreeNode(parent_folder_node=cur_node,
                                               folder_or_filename=parsed_tuple[1],
                                               is_file=True,
                                               file_size=parsed_tuple[2])
                cur_node.add_child_dir(child_node)

            elif parsed_tuple[0] == 'child_node':
                child_node = DirectoryTreeNode(parent_folder_node=cur_node,
                                               folder_or_filename=parsed_tuple[1])
                cur_node.add_child_dir(child_node)

            else:
                if parsed_tuple[1] == 'get_child_node_and_file':
                    continue
                else:
                    if parsed_tuple[2] == '/':
                        continue
                    elif parsed_tuple[2] == '..':
                        cur_node = cur_node.get_parent_folder_node()
                    else:
                        cur_node = cur_node.go_to_child_node(child_folder_name=parsed_tuple[2])

        total_size = tree_root.get_size
        unused_size = 70000000 - total_size

        min_size = 30000000
        for i in tree_root.traverse_size():
            if i + unused_size >= 30000000 and i < min_size:
                min_size = i

        return min_size


if __name__ == '__main__':
    # test_trees()
    print(get_size_of_folders())