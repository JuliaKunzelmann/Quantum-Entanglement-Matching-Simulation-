class ExperimentParams:
    """Parameters for the large-scale LP experiment."""

    # Large-N scaling grid.
    N_values = (10, 20, 30, 40, 50)
    N = 10

    # Memories per party. m=5 is intentionally omitted because
    # round(rho*m) gives poor density resolution at that scale.
    m_values = (10, 15, 20)

    # Sparse connectivity levels.
    rho_values = (0.2, 0.3, 0.4)

    # Independent memory deletion probabilities.
    p_del_values = (0.0, 0.05, 0.10, 0.20)

    # Finite truncated power-law exponent.
    power_law_gamma = 2.5

    # More independent topologies, fewer loss realizations per topology.
    # The product remains 50 realizations per parameter cell.
    num_base_graphs = 10
    num_loss_realizations = 5

    # Reproducibility.
    master_seed = 1278412

    # Use a new output file because the CSV schema differs from the
    # previous exact/ILP-capable experiment and the earlier
    # pilot that used a different heuristic runtime timer.
    output_dir = "Results_extended"
    output_file = "results_large_N50_final.csv"

    @staticmethod
    def target_degree(m, rho):
        """Return d = round(rho*m), clipped to [1, m]."""
        d = int(rho * m + 0.5)
        return max(1, min(m, d))
