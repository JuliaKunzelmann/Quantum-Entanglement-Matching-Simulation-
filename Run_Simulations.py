import csv
import os
import random
import time

import numpy as np

from def_variables import Params
from def_variables_large import ExperimentParams

from Generate_Simulation_Graphs import (
    create_sparse_random_graph,
    create_power_law_graph,
    create_fully_connected_graph,
)
from Simulation_Utils import apply_memory_loss
from Strategy_1 import Strategy_1
from Strategy_2 import Strategy_2
from Optimization import (
    cardinality_upper_bound,
    get_lp_upper_bound,
)


# Raw simulation output only stores irreducible inputs/results.
# Derived quantities such as S1/LP and S2/LP are computed later in analysis.
FIELDNAMES = [
    "graph_type",
    "N",
    "m",
    "rho",
    "p_del",
    "base_graph",
    "loss_run",
    "topology_seed",
    "deletion_seed",
    "heuristic_seed",
    "deleted_memories",
    "cardinality_upper_bound",
    "S1",
    "S2",
    "LP_upper_bound",
    "runtime_S1",
    "runtime_S2",
    "runtime_LP",
]


# ---------------------------------------------------------------------------
# Formatting and reproducibility helpers
# ---------------------------------------------------------------------------


def normalize_float(value):
    if value is None or value == "":
        return ""
    return f"{float(value):.12g}"



def normalize_integer(value):
    if value is None or value == "":
        return ""
    return str(int(value))



def simulation_key(values):
    """Return the unique resume key for one simulation realization."""
    return (
        str(values.get("graph_type", "")),
        normalize_integer(values.get("N")),
        normalize_integer(values.get("m")),
        normalize_float(values.get("rho")),
        normalize_float(values.get("p_del")),
        normalize_integer(values.get("base_graph")),
        normalize_integer(values.get("loss_run")),
        normalize_integer(values.get("topology_seed")),
        normalize_integer(values.get("deletion_seed")),
        normalize_integer(values.get("heuristic_seed")),
    )



def float_code(value):
    return int(round(float(value) * 1_000_000))



def make_seed(*parts):
    """Create a deterministic uint32 seed from the master seed and tags."""
    seed_sequence = np.random.SeedSequence(
        [
            ExperimentParams.master_seed,
            *[int(part) for part in parts],
        ]
    )
    return int(seed_sequence.generate_state(1, dtype=np.uint32)[0])



def load_completed_keys(output_path):
    """Load completed simulation keys for safe resume."""
    if not os.path.exists(output_path):
        return set()

    if os.path.getsize(output_path) == 0:
        return set()

    completed = set()

    with open(output_path, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        if reader.fieldnames != FIELDNAMES:
            raise ValueError(
                "Existing CSV has a different format. "
                "Use a new output file or remove the old file."
            )

        for row in reader:
            if any(row.get(field) is None for field in FIELDNAMES):
                continue
            completed.add(simulation_key(row))

    return completed



def write_result(writer, csvfile, result, completed_keys):
    writer.writerow(result)
    csvfile.flush()
    completed_keys.add(simulation_key(result))


# ---------------------------------------------------------------------------
# Legacy heuristic wrappers
# ---------------------------------------------------------------------------


def set_legacy_params(N, m):
    """Set the global parameters expected by the legacy heuristic code."""
    Params.N = N
    Params.m = m
    Params.m_total = N * m



def run_heuristic(strategy, matrix, seed):
    """Run one randomized legacy heuristic without modifying the input.

    Runtime is measured with time.perf_counter(), matching the LP timer, so
    all reported runtimes use the same wall-clock convention.
    """
    random.seed(seed)
    np.random.seed(seed)

    matrix_copy = matrix.copy()

    start = time.perf_counter()
    _, cardinality = strategy(matrix_copy)
    runtime = time.perf_counter() - start

    return cardinality, runtime


# ---------------------------------------------------------------------------
# One realization
# ---------------------------------------------------------------------------


def run_single_instance(
    base_matrix,
    graph_type,
    N,
    m,
    rho,
    p_del,
    base_graph_id,
    loss_id,
    topology_seed,
    deletion_seed,
    heuristic_seed,
):
    """
    Run S1, S2 and the scalable LP bound on one loss realization.

    For fully connected graphs, the LP optimum is known analytically to
    equal the cardinality upper bound, so no LP solver is invoked and
    runtime_LP is left blank (None).
    """
    set_legacy_params(N=N, m=m)

    loss_matrix, deleted_nodes = apply_memory_loss(
        base_matrix=base_matrix,
        N=N,
        m=m,
        p_del=p_del,
        seed=deletion_seed,
    )

    loss_before = loss_matrix.copy()

    cardinality_s1, runtime_s1 = run_heuristic(
        Strategy_1,
        loss_matrix,
        heuristic_seed,
    )

    cardinality_s2, runtime_s2 = run_heuristic(
        Strategy_2,
        loss_matrix,
        heuristic_seed,
    )

    # The legacy strategies must not mutate the shared loss matrix.
    assert np.array_equal(loss_matrix, loss_before)

    upper_bound = cardinality_upper_bound(
        loss_matrix,
        N=N,
        m=m,
    )

    if graph_type == "fully_connected":
        # Complete bipartite reference: the integral optimum and the LP
        # optimum both equal the cardinality bound. We store the LP value
        # for a common result schema, but no LP solver runtime is claimed.
        lp_upper_bound = float(upper_bound)
        runtime_lp = None
    else:
        start = time.perf_counter()
        lp_upper_bound, _ = get_lp_upper_bound(
            loss_matrix,
            N=N,
            m=m,
        )
        runtime_lp = time.perf_counter() - start

    # Core correctness checks.
    assert cardinality_s1 <= upper_bound
    assert cardinality_s2 <= upper_bound

    assert lp_upper_bound <= upper_bound + 1e-8
    assert cardinality_s1 <= lp_upper_bound + 1e-8
    assert cardinality_s2 <= lp_upper_bound + 1e-8

    if graph_type == "fully_connected":
        assert np.isclose(lp_upper_bound, upper_bound, atol=1e-8)

    return {
        "graph_type": graph_type,
        "N": N,
        "m": m,
        "rho": rho,
        "p_del": p_del,
        "base_graph": base_graph_id,
        "loss_run": loss_id,
        "topology_seed": topology_seed,
        "deletion_seed": deletion_seed,
        "heuristic_seed": heuristic_seed,
        "deleted_memories": len(deleted_nodes),
        "cardinality_upper_bound": upper_bound,
        "S1": cardinality_s1,
        "S2": cardinality_s2,
        "LP_upper_bound": lp_upper_bound,
        "runtime_S1": runtime_s1,
        "runtime_S2": runtime_s2,
        "runtime_LP": runtime_lp,
    }


# ---------------------------------------------------------------------------
# Sparse-random and power-law experiments
# ---------------------------------------------------------------------------


def run_sparse_simulations(writer, csvfile, completed_keys):
    written = 0
    skipped = 0

    for N in ExperimentParams.N_values:
        for m in ExperimentParams.m_values:
            for rho in ExperimentParams.rho_values:
                rho_code = float_code(rho)

                for base_graph_id in range(ExperimentParams.num_base_graphs):
                    sparse_seed = make_seed(
                        1,
                        N,
                        m,
                        rho_code,
                        base_graph_id,
                    )

                    power_law_seed = make_seed(
                        2,
                        N,
                        m,
                        rho_code,
                        base_graph_id,
                    )

                    sparse_random = create_sparse_random_graph(
                        N=N,
                        m=m,
                        rho=rho,
                        seed=sparse_seed,
                    )

                    power_law = create_power_law_graph(
                        N=N,
                        m=m,
                        rho=rho,
                        gamma=ExperimentParams.power_law_gamma,
                        seed=power_law_seed,
                    )

                    # deletion_tag and heuristic_tag keep the random streams
                    # independent across topology families.
                    graphs = [
                        (
                            "sparse_random",
                            sparse_random,
                            sparse_seed,
                            3,
                            4,
                        ),
                        (
                            "power_law",
                            power_law,
                            power_law_seed,
                            5,
                            6,
                        ),
                    ]

                    for p_del in ExperimentParams.p_del_values:
                        p_code = float_code(p_del)

                        for loss_id in range(
                            ExperimentParams.num_loss_realizations
                        ):
                            for (
                                graph_type,
                                base_matrix,
                                topology_seed,
                                deletion_tag,
                                heuristic_tag,
                            ) in graphs:
                                deletion_seed = make_seed(
                                    deletion_tag,
                                    N,
                                    m,
                                    rho_code,
                                    base_graph_id,
                                    p_code,
                                    loss_id,
                                )

                                heuristic_seed = make_seed(
                                    heuristic_tag,
                                    N,
                                    m,
                                    rho_code,
                                    base_graph_id,
                                    p_code,
                                    loss_id,
                                )

                                planned = {
                                    "graph_type": graph_type,
                                    "N": N,
                                    "m": m,
                                    "rho": rho,
                                    "p_del": p_del,
                                    "base_graph": base_graph_id,
                                    "loss_run": loss_id,
                                    "topology_seed": topology_seed,
                                    "deletion_seed": deletion_seed,
                                    "heuristic_seed": heuristic_seed,
                                }

                                key = simulation_key(planned)

                                if key in completed_keys:
                                    skipped += 1
                                    continue

                                result = run_single_instance(
                                    base_matrix=base_matrix,
                                    graph_type=graph_type,
                                    N=N,
                                    m=m,
                                    rho=rho,
                                    p_del=p_del,
                                    base_graph_id=base_graph_id,
                                    loss_id=loss_id,
                                    topology_seed=topology_seed,
                                    deletion_seed=deletion_seed,
                                    heuristic_seed=heuristic_seed,
                                )

                                write_result(
                                    writer,
                                    csvfile,
                                    result,
                                    completed_keys,
                                )
                                written += 1

                print(
                    "Finished sparse graphs: "
                    f"N={N}, m={m}, rho={rho}"
                )

    return written, skipped


# ---------------------------------------------------------------------------
# Fully connected / complete-bipartite reference
# ---------------------------------------------------------------------------


def run_fully_connected_simulations(writer, csvfile, completed_keys):
    written = 0
    skipped = 0

    for N in ExperimentParams.N_values:
        for m in ExperimentParams.m_values:
            base_matrix = create_fully_connected_graph(N=N, m=m)

            # There is no random base topology here. We nevertheless use the
            # same total number of stochastic repetitions (10*5 = 50) for
            # memory-loss and randomized-heuristic variability.
            num_runs = (
                ExperimentParams.num_base_graphs
                * ExperimentParams.num_loss_realizations
            )

            for p_del in ExperimentParams.p_del_values:
                p_code = float_code(p_del)

                for loss_id in range(num_runs):
                    deletion_seed = make_seed(
                        7,
                        N,
                        m,
                        p_code,
                        loss_id,
                    )

                    heuristic_seed = make_seed(
                        8,
                        N,
                        m,
                        p_code,
                        loss_id,
                    )

                    planned = {
                        "graph_type": "fully_connected",
                        "N": N,
                        "m": m,
                        "rho": None,
                        "p_del": p_del,
                        "base_graph": 0,
                        "loss_run": loss_id,
                        "topology_seed": None,
                        "deletion_seed": deletion_seed,
                        "heuristic_seed": heuristic_seed,
                    }

                    key = simulation_key(planned)

                    if key in completed_keys:
                        skipped += 1
                        continue

                    result = run_single_instance(
                        base_matrix=base_matrix,
                        graph_type="fully_connected",
                        N=N,
                        m=m,
                        rho=None,
                        p_del=p_del,
                        base_graph_id=0,
                        loss_id=loss_id,
                        topology_seed=None,
                        deletion_seed=deletion_seed,
                        heuristic_seed=heuristic_seed,
                    )

                    write_result(
                        writer,
                        csvfile,
                        result,
                        completed_keys,
                    )
                    written += 1

            print(f"Finished fully connected: N={N}, m={m}")

    return written, skipped


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def expected_row_counts():
    """Return expected row counts for the configured full experiment."""
    num_N = len(ExperimentParams.N_values)
    num_m = len(ExperimentParams.m_values)
    num_rho = len(ExperimentParams.rho_values)
    num_p = len(ExperimentParams.p_del_values)
    num_base = ExperimentParams.num_base_graphs
    num_loss = ExperimentParams.num_loss_realizations

    per_sparse_family = (
        num_N
        * num_m
        * num_rho
        * num_p
        * num_base
        * num_loss
    )

    fully_connected = (
        num_N
        * num_m
        * num_p
        * num_base
        * num_loss
    )

    return {
        "sparse_random": per_sparse_family,
        "power_law": per_sparse_family,
        "fully_connected": fully_connected,
        "total": 2 * per_sparse_family + fully_connected,
    }



def main():
    os.makedirs(ExperimentParams.output_dir, exist_ok=True)

    output_path = os.path.join(
        ExperimentParams.output_dir,
        ExperimentParams.output_file,
    )

    counts = expected_row_counts()

    print("Configured large-scale experiment")
    print(f"N values: {ExperimentParams.N_values}")
    print(f"m values: {ExperimentParams.m_values}")
    print(f"rho values: {ExperimentParams.rho_values}")
    print(f"p_del values: {ExperimentParams.p_del_values}")
    print(
        "Base graphs x loss realizations: "
        f"{ExperimentParams.num_base_graphs} x "
        f"{ExperimentParams.num_loss_realizations}"
    )
    print(
        "Expected rows: "
        f"sparse_random={counts['sparse_random']}, "
        f"power_law={counts['power_law']}, "
        f"fully_connected={counts['fully_connected']}, "
        f"total={counts['total']}\n"
    )

    completed_keys = load_completed_keys(output_path)

    file_exists = (
        os.path.exists(output_path)
        and os.path.getsize(output_path) > 0
    )

    print(f"Results file: {output_path}")
    print(f"Already completed runs: {len(completed_keys)}\n")

    with open(output_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=FIELDNAMES,
        )

        if not file_exists:
            writer.writeheader()
            csvfile.flush()

        sparse_written, sparse_skipped = run_sparse_simulations(
            writer,
            csvfile,
            completed_keys,
        )

        full_written, full_skipped = run_fully_connected_simulations(
            writer,
            csvfile,
            completed_keys,
        )

    written = sparse_written + full_written
    skipped = sparse_skipped + full_skipped

    print(f"\nNew simulations written: {written}")
    print(f"Existing simulations skipped: {skipped}")
    print(f"Total completed simulations: {len(completed_keys)}")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
