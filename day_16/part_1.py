import itertools
import re
import heapq
from collections import deque, OrderedDict
from copy import deepcopy
from functools import cached_property


class Valve:

    def __init__(self, name, flow_rate, connect_to):
        self.name = name
        self.flow_rate = int(flow_rate)
        self.connect_to = {i for i in connect_to.split(', ')}

    def __str__(self):
        return f"Valve {self.name} has a flow rate {self.flow_rate} and connected to {self.connect_to}"

    def pressure_released(self, min_order):
        return self.flow_rate * min_order

    def __hash__(self):
        return hash(self.name)


def test_re_match(string):
    valve = re.search(r'Valve (.*?) ', string).group(1)
    flow_rate = re.search(r'flow rate=(.*?);', string).group(1)
    connect_to = re.search(r'to (valve|valves) (.*?)$', string).group(2)
    print(valve, flow_rate, connect_to)
    return Valve(valve, flow_rate, connect_to)


def parse_file():
    valves = []
    with open("puzzle_input.txt", "r") as inputs:
        for line in inputs:
            line = line.rstrip()
            valve = test_re_match(line)
            valves.append(valve)
    return valves


class Network:

    def __init__(self, valves):
        valves_dict = {}
        for t in valves:
            valves_dict[t.name] = t
        _network_dict = OrderedDict()
        for valve in valves:
            _network_dict[valve.name] = valve.connect_to
        self.network = OrderedDict(_network_dict)
        self.lookup_table = valves_dict
        self.total_min = 30
        self.starting_point = 'AA'

    def out_edges(self, node):
        for out_node in self.network[node]:
            yield out_node, 1

    def shortest_paths(self, starting_node):
        vnum = len(self.network)
        paths = {}
        count = 0
        cands = []
        heapq.heappush(cands, (0, starting_node, starting_node))
        while count < vnum and not len(cands) == 0:
            plen, u, vmin = heapq.heappop(cands)
            if paths.get(vmin, None):
                continue
            paths[vmin] = (u, plen)
            for v, w in self.out_edges(vmin):
                if not paths.get(v, None):
                    heapq.heappush(cands, (plen + w, vmin, v))
            count += 1
        return {key: value[1] for key, value in paths.items()}, paths


class Simulation:

    def __init__(self, network):
        self.network = network
        self.valves = [v.name for k, v in network.lookup_table.items() if
                       v.name == network.starting_point or v.flow_rate != 0]

    @cached_property
    def shortest_paths(self):
        paths = {}
        for node in self.network.lookup_table:
            path, _ = self.network.shortest_paths(node)
            path = {k: v for k, v in path.items() if self.network.lookup_table[k].flow_rate != 0}
            paths[node] = path
        return paths

    # def run(self):
    #     max_pressure = 0
    #
    #     permutation = itertools.permutations(self.valves[1:])
    #
    #     while True:
    #         i = next(permutation)
    #
    #         if not i:
    #             break
    #
    #         i = [self.network.starting_point] + list(i)
    #         pressure = 0
    #         minutes = 30
    #         valves = {}
    #         for j in range(1, len(i)):
    #             minutes -= paths[i[j - 1]][i[j]]
    #             minutes -= 1
    #             pressure += network.lookup_table[i[j]].pressure_released(minutes)
    #             if minutes <= 0:
    #                 break
    #
    #         if pressure > max_pressure:
    #             max_pressure = pressure
    #             permute = i
    #             print(i, max_pressure)
    #
    #     print(max_pressure, permute)

    def run_2(self):

        print(self.shortest_paths)

        start_node = self.network.starting_point
        start_path = list(self.shortest_paths[start_node].keys())

        container = deque()
        remain_min = 30

        start_path = [i for i in filter(lambda x: remain_min - self.shortest_paths[start_node][x] - 1 > 0 and start_node != x, start_path)]
        container.append((start_node, start_path, [(start_node, remain_min)]))

        max_val = 0

        while not len(container) == 0:

            elem, out_edges, seq = container.pop()

            remain_min = seq[-1][1]

            if remain_min <= 0 or len(seq) >= len(self.valves):
                # print(seq)
                total = sum([self.network.lookup_table[i[0]].pressure_released(i[1]) for i in seq if i[1] > 0])
                if total > max_val:
                    max_val = total
                    print(seq, max_val)
                else:
                    continue

            if len(out_edges) > 0:
                edge = out_edges[-1]
                seq_ = deepcopy(seq)
                container.append((elem, [i for i in out_edges[:-1] if i not in {j[0] for j in seq_}], seq_))
                next_path = list(self.shortest_paths[edge].keys())
                if edge in [i[0] for i in seq]:
                    continue
                next_path = [i for i in filter(lambda x: x != edge and x not in {i[0] for i in seq}, next_path)]
                if not next_path:
                    next_path = []
                seq.append((edge, remain_min - 1 - self.shortest_paths[elem][edge]))
                container.append((edge, next_path, seq))
            else:
                continue

        print(container)

        print(max_val)



if __name__ == '__main__':
    valves = parse_file()
    network = Network(valves)
    simulation = Simulation(network)

    simulation.run_2()

