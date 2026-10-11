import numpy as np


def create_empty_matrix(N, m):
    return np.zeros(
        (N * m, N * m),
        dtype=int,
    )


def target_degree(m, rho):
    """
    Target mean center degree within one
    center-peer layer.
    """

    d = int(
        rho * m + 0.5
    )

    return max(
        1,
        min(m, d),
    )


def create_sparse_random_graph(
    N,
    m,
    rho,
    seed,
):
    """
    Create a sparse random multipartite router.

    For every center-peer layer, exactly

        M = m * d

    edges are sampled uniformly without replacement
    from the m^2 possible center-peer edges, where

        d = round(rho * m).

    Therefore all sparse-random graphs with the same
    (m, rho) have exactly the same edge count.
    """

    if N < 2:
        raise ValueError(
            "N must be at least 2."
        )

    if m < 1:
        raise ValueError(
            "m must be positive."
        )

    if not 0.0 <= rho <= 1.0:
        raise ValueError(
            "rho must lie in [0, 1]."
        )

    rng = np.random.default_rng(
        seed
    )

    matrix = create_empty_matrix(
        N=N,
        m=m,
    )

    d = target_degree(
        m=m,
        rho=rho,
    )

    num_edges = (
        m * d
    )

    for party in range(
        1,
        N,
    ):

        start = (
            party * m
        )

        selected = rng.choice(
            m * m,
            size=num_edges,
            replace=False,
        )

        center_indices = (
            selected // m
        )

        peer_indices = (
            selected % m
        )

        matrix[
            center_indices,
            start + peer_indices,
        ] = 1

    return matrix


def _truncated_power_law_mean(
    m,
    k_min,
    gamma,
):
    """
    Mean degree of the finite truncated power-law

        P(k) proportional to k^(-gamma)

    for

        k_min <= k <= m.
    """

    degrees = np.arange(
        k_min,
        m + 1,
        dtype=float,
    )

    weights = (
        degrees
        ** (-gamma)
    )

    weights = (
        weights
        / weights.sum()
    )

    return float(
        np.sum(
            degrees
            * weights
        )
    )


def _choose_power_law_k_min(
    m,
    target_mean,
    gamma,
):
    """
    Choose a lower cutoff k_min whose unconstrained
    truncated-power-law mean is close to target_mean.

    For target_mean > 1, k_min is kept strictly below
    target_mean whenever possible. Otherwise fixing the
    total degree to m * target_mean could force every
    degree to be identical and eliminate heterogeneity.

    Example:

        target mean = 6

    may lead to a support such as

        4 <= k <= 20

    when gamma = 2.5.
    """

    if target_mean <= 1:
        return 1

    if target_mean >= m:
        return m

    candidates = range(
        1,
        target_mean,
    )

    best_k_min = min(
        candidates,
        key=lambda k_min: (
            abs(
                _truncated_power_law_mean(
                    m=m,
                    k_min=k_min,
                    gamma=gamma,
                )
                - target_mean
            ),
            k_min,
        ),
    )

    return int(
        best_k_min
    )


def _sample_fixed_sum_truncated_power_law(
    m,
    target_mean,
    gamma,
    rng,
):
    """
    Sample a labelled center-degree sequence from

        P(d_1, ..., d_m)
        proportional to
        product_j d_j^(-gamma)

    subject to

        k_min <= d_j <= m

    and

        sum_j d_j = m * target_mean.

    The lower cutoff k_min is chosen so that the
    corresponding unconditioned truncated power law
    has a mean close to target_mean.

    Sampling is performed exactly from the resulting
    finite fixed-sum distribution using dynamic
    programming.

    This avoids MCMC burn-in and rejection sampling.
    """

    if gamma <= 0:
        raise ValueError(
            "gamma must be positive."
        )

    if m < 1:
        raise ValueError(
            "m must be positive."
        )

    if not 1 <= target_mean <= m:
        raise ValueError(
            "target_mean must lie between 1 and m."
        )

    target_sum = (
        m * target_mean
    )

    # Degenerate boundary cases.
    if target_mean == 1:

        return np.ones(
            m,
            dtype=int,
        )

    if target_mean == m:

        return np.full(
            m,
            m,
            dtype=int,
        )

    k_min = (
        _choose_power_law_k_min(
            m=m,
            target_mean=target_mean,
            gamma=gamma,
        )
    )

    degree_values = np.arange(
        k_min,
        m + 1,
        dtype=int,
    )

    weights = (
        degree_values.astype(
            float
        )
        ** (-gamma)
    )

    # Normalization is not mathematically necessary
    # for the conditional distribution, but improves
    # numerical stability.
    weights = (
        weights
        / weights.sum()
    )

    # dp[n, s] is the total probability weight of
    # assigning n labelled nodes degrees summing to s.
    dp = np.zeros(
        (
            m + 1,
            target_sum + 1,
        ),
        dtype=float,
    )

    dp[
        0,
        0,
    ] = 1.0

    for num_nodes in range(
        1,
        m + 1,
    ):

        min_sum = (
            num_nodes
            * k_min
        )

        max_sum = min(
            target_sum,
            num_nodes * m,
        )

        for degree_sum in range(
            min_sum,
            max_sum + 1,
        ):

            total_weight = 0.0

            for (
                degree,
                weight,
            ) in zip(
                degree_values,
                weights,
            ):

                previous_sum = (
                    degree_sum
                    - int(
                        degree
                    )
                )

                if previous_sum < 0:
                    break

                total_weight += (
                    float(
                        weight
                    )
                    * dp[
                        num_nodes - 1,
                        previous_sum,
                    ]
                )

            dp[
                num_nodes,
                degree_sum,
            ] = total_weight

    if (
        dp[
            m,
            target_sum,
        ]
        <= 0.0
    ):

        raise RuntimeError(
            "Could not construct a fixed-sum "
            "power-law degree distribution."
        )

    degrees = np.empty(
        m,
        dtype=int,
    )

    remaining_nodes = m
    remaining_sum = (
        target_sum
    )

    for node in range(m):

        feasible_degrees = []
        conditional_weights = []

        next_nodes = (
            remaining_nodes
            - 1
        )

        for (
            degree,
            weight,
        ) in zip(
            degree_values,
            weights,
        ):

            degree = int(
                degree
            )

            next_sum = (
                remaining_sum
                - degree
            )

            if next_sum < 0:
                continue

            min_possible = (
                next_nodes
                * k_min
            )

            max_possible = (
                next_nodes
                * m
            )

            if (
                next_sum
                < min_possible
            ):
                continue

            if (
                next_sum
                > max_possible
            ):
                continue

            continuation_weight = (
                dp[
                    next_nodes,
                    next_sum,
                ]
            )

            candidate_weight = (
                float(
                    weight
                )
                * continuation_weight
            )

            if candidate_weight <= 0.0:
                continue

            feasible_degrees.append(
                degree
            )

            conditional_weights.append(
                candidate_weight
            )

        if not feasible_degrees:
            raise RuntimeError(
                "Power-law conditional sampling failed."
            )

        probabilities = np.asarray(
            conditional_weights,
            dtype=float,
        )

        probabilities = (
            probabilities
            / probabilities.sum()
        )

        selected_degree = int(
            rng.choice(
                feasible_degrees,
                p=probabilities,
            )
        )

        degrees[
            node
        ] = selected_degree

        remaining_sum -= (
            selected_degree
        )

        remaining_nodes -= 1

    if remaining_sum != 0:
        raise RuntimeError(
            "Power-law degree sequence has "
            "an incorrect total degree."
        )

    assert (
        int(
            degrees.sum()
        )
        == target_sum
    )

    assert np.all(
        degrees >= k_min
    )

    assert np.all(
        degrees <= m
    )

    # Random permutation makes the association between
    # degree and center-memory index explicitly random.
    degrees = degrees[
        rng.permutation(
            m
        )
    ]

    return degrees


def create_power_law_graph(
    N,
    m,
    rho,
    gamma,
    seed,
):
    """
    Create a multipartite topology with a power-law
    center-degree distribution.

    For each base graph, one center-degree sequence

        d_C = (d_1, ..., d_m)

    is sampled from a finite truncated power-law model

        P(k) proportional to k^(-gamma),

    conditioned on

        sum_c d_c = m * d,

    where

        d = round(rho * m).

    The same center-degree sequence is used in every
    center-peer layer. Therefore a center memory that
    acts as a hub remains a hub with respect to all
    peer partitions.

    For each center and peer partition, d_c distinct
    peer memories are then selected uniformly at random.

    Consequently every center-peer layer contains
    exactly

        m * d

    edges, matching the edge budget of the sparse
    random topology at the same (m, rho).

    Only the center-side degree distribution is imposed
    to follow the power-law model. Peer-side degrees
    arise naturally from the random neighbor selection.
    """

    if N < 2:
        raise ValueError(
            "N must be at least 2."
        )

    if m < 1:
        raise ValueError(
            "m must be positive."
        )

    if gamma <= 0:
        raise ValueError(
            "gamma must be positive."
        )

    if not 0.0 <= rho <= 1.0:
        raise ValueError(
            "rho must lie in [0, 1]."
        )

    rng = np.random.default_rng(
        seed
    )

    matrix = create_empty_matrix(
        N=N,
        m=m,
    )

    d = target_degree(
        m=m,
        rho=rho,
    )

    center_degrees = (
        _sample_fixed_sum_truncated_power_law(
            m=m,
            target_mean=d,
            gamma=gamma,
            rng=rng,
        )
    )

    expected_edges = (
        m * d
    )

    assert (
        int(
            center_degrees.sum()
        )
        == expected_edges
    )

    for party in range(
        1,
        N,
    ):

        start = (
            party * m
        )

        for center in range(m):

            degree = int(
                center_degrees[
                    center
                ]
            )

            peer_neighbors = (
                rng.choice(
                    m,
                    size=degree,
                    replace=False,
                )
            )

            matrix[
                center,
                start
                + peer_neighbors,
            ] = 1

        block = matrix[
            :m,
            start:
            start + m,
        ]

        # Exact edge budget.
        assert (
            int(
                block.sum()
            )
            == expected_edges
        )

        # The same center-degree sequence must be
        # realized in every peer layer.
        assert np.array_equal(
            block.sum(
                axis=1
            ),
            center_degrees,
        )

    return matrix


def create_fully_connected_graph(
    N,
    m,
):
    """
    Create the complete center-peer topology.

    Every center memory is connected to every memory
    in every peer partition.
    """

    if N < 2:
        raise ValueError(
            "N must be at least 2."
        )

    if m < 1:
        raise ValueError(
            "m must be positive."
        )

    matrix = create_empty_matrix(
        N=N,
        m=m,
    )

    for party in range(
        1,
        N,
    ):

        start = (
            party * m
        )

        end = (
            (party + 1)
            * m
        )

        matrix[
            :m,
            start:end,
        ] = 1

    return matrix