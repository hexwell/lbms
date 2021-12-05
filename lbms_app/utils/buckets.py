from collections import defaultdict


def make_buckets(nodes, ancestors):
    buckets = defaultdict(set)
    sorted = set()

    # Descend lineages
    for node in nodes:
        if node not in sorted:
            ancs = ancestors(node)

            for ancestor in ancs:
                # If an ancestor is found in nodes, it downgrades all its descendants to itself
                if ancestor in nodes:
                    buckets[ancestor] |= {ancestor, *ancs}  # Add itself and all remaining descendants to bucket
                    sorted |= buckets[ancestor]  # Update sorted

                    break

    return dict(buckets)
