from collections import defaultdict


def unique(iterable):
    return len(set(iterable)) == 1


def lul(nodes, ancestors):
    """
    Finds the lowest level populated with ancestors for all nodes (lowest ubiquitous level)

    nodes: Iterable of nodes. All items must have a common ancestor
    ancestors: A function from node to an iterable of it's ancestors including itself, ordered from root to leaf.
    """

    # Lineage (ancestor chain) for each node
    lineages = map(ancestors, nodes)

    # Lineages start from a common root.
    # zip lineages so that each element of the zip is a level of the tree
    # This also stops at the shortage lineage
    levels = zip(*lineages)

    sentinel = object()
    lowest_ubiquitous_level = sentinel  # default
    for lowest_ubiquitous_level in levels:  # find last one
        pass

    if lowest_ubiquitous_level is sentinel:
        return None  # lca not found

    else:
        return set(lowest_ubiquitous_level)


def mapdict(f, d):
    return {k: f(v) for k, v in d.items()}


def hierarchies_by_root(nodes, ancestors):
    hierarchies = defaultdict(set)

    for node in nodes:
        root, *_ = ancestors(node)
        hierarchies[root].add(node)

    return hierarchies


def buckets(hierarchies, nodes, ancestors):
    translation_table = defaultdict(set)

    for node in nodes:
        ancs = root, *_ = tuple(ancestors(node))

        for possible_ancestor in hierarchies[root]:
            if possible_ancestor in ancs:
                translation_table[possible_ancestor].add(node)
                break

    for bucket_root in translation_table:
        translation_table[bucket_root].add(bucket_root)

    return translation_table


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


    def translate(hierarchies, nodes, ancestors):
        translation_table = buckets(hierarchies, nodes, ancestors)

        return (translation_table[node] for node in nodes)


    s = 'dffdfiicic'
    s = 'cb'

    i = mapdict(lambda nodes: lul(nodes, ancstrs), hierarchies_by_root(s, ancstrs))

    print(list(translate(i, s, ancstrs)))
