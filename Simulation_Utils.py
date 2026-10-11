import numpy as np


def apply_memory_loss(
    base_matrix,
    N,
    m,
    p_del,
    seed,
):
    """
    Apply independent memory loss to one graph realization.

    Each active memory is deleted independently with probability p_del.

    Deleting a center memory removes its complete row.
    Deleting a peer memory removes its complete column.

    The input matrix is not modified.

    Returns
    -------
    matrix_after_loss : np.ndarray
        Copy of the graph after memory loss.

    deleted_nodes : list[int]
        Global indices of deleted memories.
    """

    if not 0.0 <= p_del <= 1.0:
        raise ValueError("p_del must be between 0 and 1.")

    expected_shape = (N * m, N * m)

    if base_matrix.shape != expected_shape:
        raise ValueError(
            f"Expected matrix shape {expected_shape}, "
            f"got {base_matrix.shape}."
        )

    rng = np.random.default_rng(seed)

    # Important: never modify the base graph.
    matrix = base_matrix.copy()

    active_nodes = []

    # Active center memories:
    # at least one connection to a peer.
    for center in range(m):
        if np.any(base_matrix[center, m:]):
            active_nodes.append(center)

    # Active peer memories:
    # at least one incoming connection from the center.
    for peer in range(m, N * m):
        if np.any(base_matrix[:m, peer]):
            active_nodes.append(peer)

    deleted_nodes = []

    for node in active_nodes:

        if rng.random() < p_del:

            deleted_nodes.append(node)

            if node < m:
                # Center memory:
                # remove all outgoing compatibility edges.
                matrix[node, :] = 0

            else:
                # Peer memory:
                # remove all incoming compatibility edges.
                matrix[:, node] = 0

    return matrix, deleted_nodes