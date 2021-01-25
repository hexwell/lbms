from collections import defaultdict
from itertools import takewhile


def unique(iterable):
    return len(set(iterable)) == 1


def lca(nodes, ancestors):
    """
    Finds the lowest common ancestor between nodes

    nodes: Iterable of nodes. All items must have a common ancestor
    ancestors: A function from node to an iterable of it's ancestors including itself, ordered from root to leaf.
    """

    # Lineage (ancestor chain) for each node
    lineages = map(ancestors, nodes)

    # Lineages start from a common root.
    # zip lineages so that each element of the zip is a level of the tree
    levels = zip(*lineages)

    # Common levels have just one node in them
    common_levels = takewhile(unique, levels)

    sentinel = object()
    lowest_common_level = sentinel  # default
    for lowest_common_level in common_levels:  # find last one
        pass

    if lowest_common_level is sentinel:
        return None  # lca not found

    else:
        return lowest_common_level[0]


def mapdict(f, d):
    return {k: f(v) for k, v in d.items()}


def hierarchies_by_root(nodes, ancestors):
    hierarchies = defaultdict(set)

    for node in nodes:
        root, *_ = ancestors(node)
        hierarchies[root].add(node)

    return hierarchies


if __name__ == '__main__':
    def ancstrs(t):
        hierarchy = {
            'a': None,
            'b': 'a',
            'c': 'a',
            'd': 'c',
            'e': None,
            'f': 'e',
            'g': 'e',
            'h': 'g',
            'i': 'f'
        }

        if hierarchy[t]:
            yield from ancstrs(hierarchy[t])

        yield t


    def translate(t, st, ancestors):
        return (t[tuple(ancestors(x))[0]] for x in st)


    s = 'dffdfiicic'

    i = mapdict(lambda nodes: lca(nodes, ancstrs), hierarchies_by_root(s, ancstrs))

    print(list(translate(i, s, ancstrs)))
