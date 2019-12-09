# coding: utf-8

data = open('day6.data').read().splitlines()
data = [pair.split(')') for pair in data]

# Construct tree as adjacency dict
tree = {}
for pair in data:
    parent, child = pair
    if not parent in tree.keys():
        tree[parent] = [child]
        continue

    tree[parent].append(child)

def count_orbits(tree, node, depth=0):
    node_direct, node_indirect =  1, depth - 1
    total_direct, total_indirect = node_direct, node_indirect

    if node in tree.keys():
        # root node
        if not depth:
            node_direct, node_indirect = 0, 0
            total_direct, total_indirect = node_direct, node_indirect

        children = tree[node]

        for child in children:
            child_direct, child_indirect = count_orbits(tree, child, depth+1)
            total_direct += child_direct
            total_indirect += child_indirect

    return total_direct, total_indirect

part1 = sum(count_orbits(tree, 'COM'))
assert part1 == 223251

def shortest_path_BFS(graph, source, destination):
    visited = []
    queue = [ [source] ]

    while len(queue):
        path = queue.pop(0)
        node = path[-1]

        if node in visited:
            continue

        visited.append(node)
        for child in graph[node]:
            new_path = list(path) + [child]

            if child == destination:
                return new_path

            queue.append(new_path)
            
    raise Exception("No path found")


# Construct non-oriented tree as adjacency dict
graph = {}
for pair in data:
    parent, child = pair
    if not parent in graph.keys():
        graph[parent] = [child]
    else:
        graph[parent].append(child)

    if not child in graph.keys():
        graph[child] = [parent]
    else:
        graph[child].append(parent)

path = shortest_path_BFS(graph, 'YOU', 'SAN')
part2 = len(path) - 1 - 1 - 1 # Substract YOU, SAN, and starting node (YOU's parent)
assert(part2 == 430)