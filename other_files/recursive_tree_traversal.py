"""
This function is not being used because the trees we need to traverse are so deep
that we need to go way beyond pythons maximum stack depth. The stack depth of
python is configurable but above some limit python starts behaving weirdly
and failing in unexpected ways. So this function is just for reference.
"""

import numpy as np


def compute_pairs_recursive(labels, edge_weights, neighborhood, edge_tree, edge_tree_idx, pos_pairs, neg_pairs):

    # extract current edge and its children
    linear_edge_index, child_1, child_2 = edge_tree[edge_tree_idx, :]
    k, d_1, w_1, h_1 = np.unravel_index(linear_edge_index, edge_weights.shape)

    # CHILD 1
    if child_1 == -1:
        # first child is a voxel.  Compute its location
        region_counts_1 = {labels[d_1, w_1, h_1]: 1}
    else:
        # recurse first child
        region_counts_1 = compute_pairs_recursive(labels, edge_weights, neighborhood,
                                                  edge_tree, child_1, pos_pairs, neg_pairs)

    # CHILD 2
    if child_2 == -1:
        # second child is a voxel.  Compute its location via neighborhood.
        offset = neighborhood[k, :]
        d_2, w_2, h_2 = (o + d for o, d in zip(offset, (d_1, w_1, h_1)))
        region_counts_2 = {labels[d_2, w_2, h_2]: 1}
    else:
        # recurse second child
        region_counts_2 = compute_pairs_recursive(labels, edge_weights, neighborhood,
                                                  edge_tree, child_2, pos_pairs, neg_pairs)

    # compute MALIS counts
    return_dict = {}
    for key1, counts1 in region_counts_1.items():
        for key2, counts2 in region_counts_2.items():
            if key1 == key2 \
               and not key1 == 0 \
               and not key2 == 0:
                pos_pairs[k, d_1, w_1, h_1] += counts1 * counts2
            else:
                neg_pairs[k, d_1, w_1, h_1] += counts1 * counts2

    for key1, counts1 in region_counts_1.items():
        return_dict[key1] = counts1

    for key2, counts2 in region_counts_2.items():
        if key2 in return_dict.keys():
            return_dict[key2] += counts2
        else:
            return_dict[key2] = counts2

    return return_dict
