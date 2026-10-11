import itertools

import numpy as np

from scipy.optimize import (
    milp,
    linprog,
    Bounds,
    LinearConstraint,
)

from scipy.sparse import (
    csc_matrix,
    lil_matrix,
)

from def_variables import Params
from Strategy_exact import get_exact_l


def cardinality_upper_bound(
    matrix,
    N,
    m,
):
    """
    Upper bound given by the minimum number of active
    memories among all partitions.
    """

    active_counts = []

    # Active center memories.
    active_center = np.any(
        matrix[
            :m,
            m:,
        ] != 0,
        axis=1,
    )

    active_counts.append(
        int(
            active_center.sum()
        )
    )

    # Active peer memories.
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

        active_peer = np.any(
            matrix[
                :m,
                start:end,
            ] != 0,
            axis=0,
        )

        active_counts.append(
            int(
                active_peer.sum()
            )
        )

    return min(
        active_counts
    )


def get_valid_hyperedges(
    matrix,
    N,
    m,
):
    """
    Generate all valid multipartite hyperedges.

    A valid hyperedge contains:
        - one center memory,
        - exactly one compatible memory from every
          peer partition.
    """

    valid_hyperedges = []

    for center in range(m):

        neighbors_per_peer = []

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

            neighbors = [
                node
                for node in range(
                    start,
                    end,
                )
                if matrix[
                    center,
                    node,
                ] == 1
            ]

            if not neighbors:
                neighbors_per_peer = []
                break

            neighbors_per_peer.append(
                neighbors
            )

        if not neighbors_per_peer:
            continue

        for peers in itertools.product(
            *neighbors_per_peer
        ):

            valid_hyperedges.append(
                (
                    center,
                    *peers,
                )
            )

    return valid_hyperedges


def get_optimum_small(
    matrix,
    N,
    m,
    heuristic_values=None,
):
    """
    Determine the true optimum using the existing
    exact algorithm.
    """

    Params.N = N
    Params.m = m
    Params.m_total = (
        N * m
    )

    upper_bound = (
        cardinality_upper_bound(
            matrix,
            N=N,
            m=m,
        )
    )

    if upper_bound == 0:
        return (
            0,
            "upper_bound",
        )

    if heuristic_values is not None:

        if len(
            heuristic_values
        ) > 0:

            if (
                max(
                    heuristic_values
                )
                == upper_bound
            ):

                return (
                    upper_bound,
                    "upper_bound",
                )

    optimum = get_exact_l(
        matrix.copy()
    )

    return (
        optimum,
        "exact",
    )


def get_optimum_ilp(
    matrix,
    N,
    m,
    heuristic_values=None,
):
    """
    Determine the true optimum using a hyperedge ILP.

    This method is intended only for instances where
    hyperedge enumeration remains tractable.
    """

    upper_bound = (
        cardinality_upper_bound(
            matrix,
            N=N,
            m=m,
        )
    )

    if upper_bound == 0:
        return (
            0,
            "upper_bound",
        )

    if heuristic_values is not None:

        if len(
            heuristic_values
        ) > 0:

            if (
                max(
                    heuristic_values
                )
                == upper_bound
            ):

                return (
                    upper_bound,
                    "upper_bound",
                )

    hyperedges = (
        get_valid_hyperedges(
            matrix,
            N=N,
            m=m,
        )
    )

    if not hyperedges:
        return (
            0,
            "ilp",
        )

    num_hyperedges = len(
        hyperedges
    )

    num_nodes = (
        N * m
    )

    # scipy.optimize.milp minimizes.
    # Therefore maximize sum(x_e) by minimizing
    # -sum(x_e).
    c = -np.ones(
        num_hyperedges,
        dtype=float,
    )

    rows = []
    cols = []
    data = []

    for (
        edge_index,
        hyperedge,
    ) in enumerate(
        hyperedges
    ):

        for node in hyperedge:

            rows.append(
                node
            )

            cols.append(
                edge_index
            )

            data.append(
                1.0
            )

    incidence = csc_matrix(
        (
            data,
            (
                rows,
                cols,
            ),
        ),
        shape=(
            num_nodes,
            num_hyperedges,
        ),
    )

    constraints = (
        LinearConstraint(
            incidence,
            lb=-np.inf,
            ub=1.0,
        )
    )

    bounds = Bounds(
        lb=np.zeros(
            num_hyperedges
        ),
        ub=np.ones(
            num_hyperedges
        ),
    )

    integrality = np.ones(
        num_hyperedges,
        dtype=int,
    )

    result = milp(
        c=c,
        integrality=integrality,
        bounds=bounds,
        constraints=constraints,
        options={
            "disp": False,
        },
    )

    if not result.success:
        raise RuntimeError(
            "ILP solver failed: "
            f"{result.message}"
        )

    optimum = int(
        round(
            -result.fun
        )
    )

    return (
        optimum,
        "ilp",
    )


def get_lp_upper_bound(
    matrix,
    N,
    m,
):
    """
    Reviewer-style edge-variable LP relaxation.

    Variables
    ---------
    z_c in [0, 1]
        Fractional use of center memory c.

    y_(c,p) in [0, 1]
        Fractional use of an existing center-peer edge.

    Constraints
    -----------
    For every center c and every peer partition P_i:

        sum_{p in P_i} y_(c,p) = z_c

    For every peer memory p:

        sum_c y_(c,p) <= 1

    Objective
    ---------
        maximize sum_c z_c

    The LP optimum upper-bounds the integral matching
    optimum.
    """

    upper_bound = (
        cardinality_upper_bound(
            matrix,
            N=N,
            m=m,
        )
    )

    if upper_bound == 0:
        return (
            0.0,
            "lp",
        )

    edge_variables = []

    for center in range(m):

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

            for peer in range(
                start,
                end,
            ):

                if matrix[
                    center,
                    peer,
                ] == 1:

                    edge_variables.append(
                        (
                            center,
                            party,
                            peer,
                        )
                    )

    num_y = len(
        edge_variables
    )

    num_z = m

    num_variables = (
        num_y
        + num_z
    )

    def z_index(center):
        return (
            num_y
            + center
        )

    # Maximize sum(z_c) by minimizing -sum(z_c).
    c = np.zeros(
        num_variables,
        dtype=float,
    )

    c[
        num_y:
    ] = -1.0

    # Equality constraints:
    #
    # sum y_(c,p) - z_c = 0
    #
    # for each center and each peer partition.
    num_equalities = (
        m
        * (N - 1)
    )

    A_eq = lil_matrix(
        (
            num_equalities,
            num_variables,
        ),
        dtype=float,
    )

    b_eq = np.zeros(
        num_equalities,
        dtype=float,
    )

    for center in range(m):

        for party in range(
            1,
            N,
        ):

            row = (
                center
                * (N - 1)
                + (
                    party - 1
                )
            )

            A_eq[
                row,
                z_index(
                    center
                ),
            ] = -1.0

    for (
        y_index,
        (
            center,
            party,
            peer,
        ),
    ) in enumerate(
        edge_variables
    ):

        row = (
            center
            * (N - 1)
            + (
                party - 1
            )
        )

        A_eq[
            row,
            y_index,
        ] = 1.0

    # Inequality constraints:
    #
    # Each peer memory may be used at most once.
    num_peer_nodes = (
        (N - 1)
        * m
    )

    A_ub = lil_matrix(
        (
            num_peer_nodes,
            num_variables,
        ),
        dtype=float,
    )

    b_ub = np.ones(
        num_peer_nodes,
        dtype=float,
    )

    for (
        y_index,
        (
            center,
            party,
            peer,
        ),
    ) in enumerate(
        edge_variables
    ):

        peer_row = (
            peer - m
        )

        A_ub[
            peer_row,
            y_index,
        ] = 1.0

    result = linprog(
        c=c,
        A_ub=csc_matrix(
            A_ub
        ),
        b_ub=b_ub,
        A_eq=csc_matrix(
            A_eq
        ),
        b_eq=b_eq,
        bounds=(
            0.0,
            1.0,
        ),
        method="highs",
    )

    if not result.success:
        raise RuntimeError(
            "LP solver failed: "
            f"{result.message}"
        )

    lp_value = float(
        -result.fun
    )

    # Numerical cleanup.
    if np.isclose(
        lp_value,
        round(
            lp_value
        ),
        atol=1e-10,
    ):

        lp_value = float(
            round(
                lp_value
            )
        )

    if (
        lp_value
        > upper_bound
        and np.isclose(
            lp_value,
            upper_bound,
            atol=1e-8,
        )
    ):

        lp_value = float(
            upper_bound
        )

    return (
        lp_value,
        "lp",
    )


def get_optimum(
    matrix,
    N,
    m,
    graph_type,
    heuristic_values=None,
    exact_max_m=5,
):
    """
    Determine the true integral optimum for instances
    where exact optimization is intended.
    """

    upper_bound = (
        cardinality_upper_bound(
            matrix,
            N=N,
            m=m,
        )
    )

    if upper_bound == 0:
        return (
            0,
            "upper_bound",
        )

    if heuristic_values is not None:

        if len(
            heuristic_values
        ) > 0:

            if (
                max(
                    heuristic_values
                )
                == upper_bound
            ):

                return (
                    upper_bound,
                    "upper_bound",
                )

    if (
        graph_type
        == "fully_connected"
    ):

        return (
            upper_bound,
            "fully_connected",
        )

    if m <= exact_max_m:

        optimum, _ = (
            get_optimum_small(
                matrix,
                N=N,
                m=m,
                heuristic_values=None,
            )
        )

        return (
            optimum,
            "exact",
        )

    optimum, _ = (
        get_optimum_ilp(
            matrix,
            N=N,
            m=m,
            heuristic_values=None,
        )
    )

    return (
        optimum,
        "ilp",
    )