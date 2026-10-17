import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import t


EXPECTED_ROWS = 21000

N_VALUES = (10, 20, 30, 40, 50)
M_VALUES = (10, 15, 20)
RHO_VALUES = (0.2, 0.3, 0.4)
P_DEL_VALUES = (0.0, 0.05, 0.10, 0.20)

# Main certified-quality figure uses m=20 because this regime remains
# non-degenerate across the tested N values. Full results for every m, rho,
# and p_del are still written to CSV tables.
MAIN_QUALITY_M = 20

# Main feasibility figure uses Sparse Random only. It shows the full tested
# density and memory-loss grid: rows are rho, columns are p_del, and each
# panel compares m=10, 15, and 20 as N grows. Power-law feasibility remains
# available in the detailed CSV table but is not repeated as a nearly-flat
# 3x4 main-paper figure.

SPARSE_TOPOLOGIES = (
    "sparse_random",
    "power_law",
)

ALL_TOPOLOGIES = (
    "sparse_random",
    "power_law",
    "fully_connected",
)

TOPOLOGY_LABELS = {
    "sparse_random": "Sparse Random",
    "power_law": "Power-Law Center-Degree",
    "fully_connected": "Fully Connected (Complete Bipartite)",
}

REQUIRED_COLUMNS = {
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
}

TOL = 1e-8


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Analyze large-scale quantum-router matching simulation results "
            "using heuristic yields and the edge-based LP upper bound."
        )
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Input results CSV. If omitted, common result-file locations are tried.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="Results_extended",
        help="Directory for summary tables and figures (default: Results_extended).",
    )
    return parser.parse_args()


def resolve_input_path(user_path):
    if user_path is not None:
        path = Path(user_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file does not exist: {path}")
        return path

    candidates = (
        Path("Results_extended/results_large_N50_final.csv"),
        Path("results_large_N50_final.csv"),
        Path("Results_extended/results_large_N50.csv"),
        Path("results_large_N50.csv"),
    )

    for path in candidates:
        if path.exists():
            return path

    raise FileNotFoundError(
        "No large-scale results CSV found.\n"
        "For example:\n"
        "python3 Analyze_Results.py --input results_large_N50_final.csv"
    )


def validate_columns(df):
    missing = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))


def add_derived_columns(df):
    df = df.copy()

    df["total_nodes"] = df["N"] * df["m"]
    df["yield_S1"] = df["S1"] / df["m"]
    df["yield_S2"] = df["S2"] / df["m"]
    df["best_heuristic"] = df[["S1", "S2"]].max(axis=1)

    positive_lp = df["LP_upper_bound"] > TOL
    df["positive_LP"] = positive_lp.astype(float)

    # S/LP is a certified lower bound on S/OPT because OPT <= LP.
    # It is undefined when LP == 0, so zero-LP instances remain NaN here and
    # are analyzed separately through feasibility/yield statistics.
    df["quality_lb_S1"] = np.where(
        positive_lp,
        df["S1"] / df["LP_upper_bound"],
        np.nan,
    )
    df["quality_lb_S2"] = np.where(
        positive_lp,
        df["S2"] / df["LP_upper_bound"],
        np.nan,
    )

    df["winner"] = np.where(
        df["S1"] > df["S2"],
        "S1",
        np.where(df["S2"] > df["S1"], "S2", "tie"),
    )

    return df


def confidence_summary_from_clusters(cluster_df, group_cols, value_col="value"):
    rows = []
    grouped = cluster_df.groupby(group_cols, dropna=False, sort=True)

    for keys, group in grouped:
        if not isinstance(keys, tuple):
            keys = (keys,)

        values = group[value_col].dropna().to_numpy(dtype=float)
        n = len(values)

        if n == 0:
            mean = np.nan
            sd = np.nan
            sem = np.nan
            ci95 = np.nan
        elif n == 1:
            mean = float(values[0])
            sd = np.nan
            sem = np.nan
            ci95 = np.nan
        else:
            mean = float(np.mean(values))
            sd = float(np.std(values, ddof=1))
            sem = sd / np.sqrt(n)
            ci95 = float(t.ppf(0.975, df=n - 1) * sem)

        row = dict(zip(group_cols, keys))
        row.update(
            {
                "mean": mean,
                "sd": sd,
                "sem": sem,
                "ci95": ci95,
                "n_clusters": n,
            }
        )
        rows.append(row)

    return pd.DataFrame(rows)


def clustered_summary(long_df, group_cols, cluster_cols, value_col="value"):
    cluster_group_cols = group_cols + cluster_cols
    cluster_df = (
        long_df.groupby(cluster_group_cols, dropna=False, sort=True)[value_col]
        .mean()
        .reset_index()
    )

    return confidence_summary_from_clusters(
        cluster_df=cluster_df,
        group_cols=group_cols,
        value_col=value_col,
    )


def write_sanity_report(df, output_dir):
    key_cols = [
        "graph_type",
        "N",
        "m",
        "rho",
        "p_del",
        "base_graph",
        "loss_run",
    ]

    duplicate_count = int(df.duplicated(subset=key_cols).sum())
    known_lp = df["LP_upper_bound"].notna()

    sparse = df[df["graph_type"].isin(SPARSE_TOPOLOGIES)].copy()
    full = df[df["graph_type"] == "fully_connected"].copy()

    runtime_columns = ["runtime_S1", "runtime_S2", "runtime_LP"]

    checks = {
        "rows": len(df),
        "expected_rows": EXPECTED_ROWS,
        "duplicates": duplicate_count,
        "missing_LP_upper_bound": int(df["LP_upper_bound"].isna().sum()),
        "S1_gt_cardinality_upper_bound": int(
            (df["S1"] > df["cardinality_upper_bound"] + TOL).sum()
        ),
        "S2_gt_cardinality_upper_bound": int(
            (df["S2"] > df["cardinality_upper_bound"] + TOL).sum()
        ),
        "S1_gt_LP": int(
            (known_lp & (df["S1"] > df["LP_upper_bound"] + TOL)).sum()
        ),
        "S2_gt_LP": int(
            (known_lp & (df["S2"] > df["LP_upper_bound"] + TOL)).sum()
        ),
        "LP_gt_cardinality_upper_bound": int(
            (
                known_lp
                & (
                    df["LP_upper_bound"]
                    > df["cardinality_upper_bound"] + TOL
                )
            ).sum()
        ),
        "negative_LP": int((df["LP_upper_bound"] < -TOL).sum()),
        "zero_LP_with_positive_S1_or_S2": int(
            (
                (df["LP_upper_bound"].abs() <= TOL)
                & ((df["S1"] > 0) | (df["S2"] > 0))
            ).sum()
        ),
        "pdel0_deleted_memories_nonzero": int(
            (
                np.isclose(df["p_del"], 0.0)
                & (df["deleted_memories"] != 0)
            ).sum()
        ),
        "negative_runtime_S1": int((df["runtime_S1"] < 0).sum()),
        "negative_runtime_S2": int((df["runtime_S2"] < 0).sum()),
        "negative_runtime_LP": int((df["runtime_LP"].dropna() < 0).sum()),
        "sparse_missing_runtime_LP": int(sparse["runtime_LP"].isna().sum()),
        "fully_connected_has_runtime_LP": int(full["runtime_LP"].notna().sum()),
        "fully_connected_S1_ne_upper_bound": int(
            (
                np.abs(full["S1"] - full["cardinality_upper_bound"])
                > TOL
            ).sum()
        ),
        "fully_connected_S2_ne_upper_bound": int(
            (
                np.abs(full["S2"] - full["cardinality_upper_bound"])
                > TOL
            ).sum()
        ),
        "fully_connected_LP_ne_upper_bound": int(
            (
                np.abs(
                    full["LP_upper_bound"]
                    - full["cardinality_upper_bound"]
                )
                > TOL
            ).sum()
        ),
    }

    # Explicitly verify that the runtime columns themselves are present and
    # finite wherever they are expected to be measured.
    checks["missing_runtime_S1"] = int(df["runtime_S1"].isna().sum())
    checks["missing_runtime_S2"] = int(df["runtime_S2"].isna().sum())
    checks["nonfinite_runtime_S1"] = int(
        (~np.isfinite(df["runtime_S1"].to_numpy(dtype=float))).sum()
    )
    checks["nonfinite_runtime_S2"] = int(
        (~np.isfinite(df["runtime_S2"].to_numpy(dtype=float))).sum()
    )

    pd.DataFrame(
        {
            "check": list(checks.keys()),
            "value": list(checks.values()),
        }
    ).to_csv(output_dir / "sanity_checks.csv", index=False)

    serious_keys = (
        "duplicates",
        "missing_LP_upper_bound",
        "S1_gt_cardinality_upper_bound",
        "S2_gt_cardinality_upper_bound",
        "S1_gt_LP",
        "S2_gt_LP",
        "LP_gt_cardinality_upper_bound",
        "negative_LP",
        "zero_LP_with_positive_S1_or_S2",
        "pdel0_deleted_memories_nonzero",
        "negative_runtime_S1",
        "negative_runtime_S2",
        "negative_runtime_LP",
        "sparse_missing_runtime_LP",
        "fully_connected_has_runtime_LP",
        "fully_connected_S1_ne_upper_bound",
        "fully_connected_S2_ne_upper_bound",
        "fully_connected_LP_ne_upper_bound",
        "missing_runtime_S1",
        "missing_runtime_S2",
        "nonfinite_runtime_S1",
        "nonfinite_runtime_S2",
    )

    serious_failures = {
        key: checks[key]
        for key in serious_keys
        if checks[key] != 0
    }

    print("\nSanity checks:")
    for key, value in checks.items():
        print(f"  {key}: {value}")

    if serious_failures:
        raise ValueError(f"Sanity check failed: {serious_failures}")

    if len(df) != EXPECTED_ROWS:
        print(f"\nWARNING: row count differs from expected {EXPECTED_ROWS}.")


def save_parameter_coverage(df, output_dir):
    coverage = (
        df.groupby(
            ["graph_type", "N", "m", "rho", "p_del"],
            dropna=False,
        )
        .size()
        .reset_index(name="rows")
    )
    coverage.to_csv(output_dir / "parameter_coverage.csv", index=False)


def create_certified_quality_summary(df, output_dir):
    data = df[
        df["graph_type"].isin(ALL_TOPOLOGIES)
        & (df["LP_upper_bound"] > TOL)
    ].copy()

    long_df = data.melt(
        id_vars=[
            "graph_type",
            "N",
            "m",
            "rho",
            "p_del",
            "base_graph",
            "loss_run",
        ],
        value_vars=["quality_lb_S1", "quality_lb_S2"],
        var_name="strategy",
        value_name="value",
    )
    long_df["strategy"] = long_df["strategy"].map(
        {
            "quality_lb_S1": "S1",
            "quality_lb_S2": "S2",
        }
    )

    # Full detailed table: each base graph is the independent topology cluster;
    # the five loss/heuristic repetitions are averaged within that cluster.
    detailed = clustered_summary(
        long_df=long_df,
        group_cols=["graph_type", "N", "m", "rho", "p_del", "strategy"],
        cluster_cols=["base_graph"],
    )
    detailed.to_csv(
        output_dir / "certified_quality_detailed.csv",
        index=False,
    )

    # Main paper figure: m=20 is used to avoid the severe feasibility-selection
    # effect that occurs for m=10 in the extremely sparse rho=0.2 regime.
    # rho and p_del remain equally weighted analysis conditions.
    main_data = long_df[long_df["m"] == MAIN_QUALITY_M].copy()
    main_summary = clustered_summary(
        long_df=main_data,
        group_cols=["graph_type", "N", "strategy"],
        cluster_cols=["rho", "p_del", "base_graph"],
    )
    main_summary.to_csv(
        output_dir / f"certified_quality_main_m{MAIN_QUALITY_M}.csv",
        index=False,
    )

    return detailed, main_summary


def create_feasibility_summary(df, output_dir):
    data = df[df["graph_type"].isin(SPARSE_TOPOLOGIES)].copy()

    # Full feasibility table for both sparse topology families. For each base
    # topology, average the five loss/heuristic realizations first; uncertainty
    # is then computed across the 10 independent base topologies.
    detailed = clustered_summary(
        long_df=data,
        group_cols=["graph_type", "N", "m", "rho", "p_del"],
        cluster_cols=["base_graph"],
        value_col="positive_LP",
    )
    detailed = detailed.rename(columns={"mean": "positive_LP_rate"})
    detailed["zero_LP_rate"] = 1.0 - detailed["positive_LP_rate"]
    detailed.to_csv(
        output_dir / "feasibility_detailed.csv",
        index=False,
    )

    # Main-paper feasibility figure: Sparse Random only, using the full
    # rho x p_del parameter grid. Power-law results remain in the detailed
    # table and can be reported in text or supplementary material.
    main = detailed[
        detailed["graph_type"] == "sparse_random"
    ].copy()

    main.to_csv(
        output_dir / "feasibility_sparse_random_main.csv",
        index=False,
    )

    return detailed, main

def make_yield_cluster_id(df):
    cluster_ids = []

    for row in df.itertuples():
        if row.graph_type == "fully_connected":
            # Fully connected has no random base topology. Its loss_run values
            # are independent loss/heuristic realizations.
            value = f"N{row.N}_m{row.m}_run{row.loss_run}"
        else:
            # Sparse families use the base graph as the independent topology
            # cluster; repetitions are averaged within each base graph.
            value = (
                f"N{row.N}_m{row.m}_rho{row.rho}_base{row.base_graph}"
            )
        cluster_ids.append(value)

    return cluster_ids


def create_yield_summary(df, output_dir):
    data = df.copy()
    data["yield_cluster"] = make_yield_cluster_id(data)

    long_df = data.melt(
        id_vars=["graph_type", "p_del", "yield_cluster"],
        value_vars=["yield_S1", "yield_S2"],
        var_name="strategy",
        value_name="value",
    )
    long_df["strategy"] = long_df["strategy"].map(
        {
            "yield_S1": "S1",
            "yield_S2": "S2",
        }
    )

    summary = clustered_summary(
        long_df=long_df,
        group_cols=["graph_type", "p_del", "strategy"],
        cluster_cols=["yield_cluster"],
    )
    summary.to_csv(
        output_dir / "matching_yield_overview.csv",
        index=False,
    )

    return summary


def save_win_rate_tables(df, output_dir):
    def make_table(data, group_cols):
        counts = (
            data.groupby(group_cols + ["winner"], dropna=False)
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )

        for column in ("S1", "tie", "S2"):
            if column not in counts:
                counts[column] = 0

        counts["total"] = counts["S1"] + counts["tie"] + counts["S2"]
        counts["S1_win_rate"] = counts["S1"] / counts["total"]
        counts["tie_rate"] = counts["tie"] / counts["total"]
        counts["S2_win_rate"] = counts["S2"] / counts["total"]
        counts["S1_not_worse_rate"] = (
            counts["S1"] + counts["tie"]
        ) / counts["total"]
        return counts

    overall = make_table(df, ["graph_type"])
    by_N = make_table(df, ["graph_type", "N"])

    overall.to_csv(
        output_dir / "win_rate_by_topology.csv",
        index=False,
    )
    by_N.to_csv(
        output_dir / "win_rate_by_topology_N.csv",
        index=False,
    )


def save_density_summaries(df, output_dir):
    sparse = df[
        df["graph_type"].isin(SPARSE_TOPOLOGIES)
    ].copy()

    positive = sparse[sparse["LP_upper_bound"] > TOL].copy()
    quality_long = positive.melt(
        id_vars=[
            "graph_type",
            "N",
            "m",
            "rho",
            "base_graph",
        ],
        value_vars=["quality_lb_S1", "quality_lb_S2"],
        var_name="strategy",
        value_name="value",
    )
    quality_long["strategy"] = quality_long["strategy"].map(
        {
            "quality_lb_S1": "S1",
            "quality_lb_S2": "S2",
        }
    )

    quality_by_density = clustered_summary(
        long_df=quality_long,
        group_cols=["graph_type", "N", "m", "rho", "strategy"],
        cluster_cols=["base_graph"],
    )
    quality_by_density.to_csv(
        output_dir / "certified_quality_by_density.csv",
        index=False,
    )

    feasibility_by_density = clustered_summary(
        long_df=sparse,
        group_cols=["graph_type", "N", "m", "rho"],
        cluster_cols=["base_graph"],
        value_col="positive_LP",
    )
    feasibility_by_density = feasibility_by_density.rename(
        columns={"mean": "positive_LP_rate"}
    )
    feasibility_by_density["zero_LP_rate"] = (
        1.0 - feasibility_by_density["positive_LP_rate"]
    )
    feasibility_by_density.to_csv(
        output_dir / "feasibility_by_density.csv",
        index=False,
    )


def save_runtime_summary(df, output_dir):
    rows = []

    for (graph_type, N, m), group in df.groupby(
        ["graph_type", "N", "m"],
        dropna=False,
    ):
        for metric in (
            "runtime_S1",
            "runtime_S2",
            "runtime_LP",
        ):
            values = group[metric].dropna().to_numpy(dtype=float)
            if len(values) == 0:
                continue

            rows.append(
                {
                    "graph_type": graph_type,
                    "N": N,
                    "m": m,
                    "total_nodes": N * m,
                    "metric": metric,
                    "n": len(values),
                    "mean": float(np.mean(values)),
                    "median": float(np.median(values)),
                    "q25": float(np.percentile(values, 25)),
                    "q75": float(np.percentile(values, 75)),
                    "p95": float(np.percentile(values, 95)),
                    "max": float(np.max(values)),
                }
            )

    pd.DataFrame(rows).to_csv(
        output_dir / "runtime_summary.csv",
        index=False,
    )


def save_figure(fig, output_dir, name):
    fig.savefig(
        output_dir / f"{name}.png",
        dpi=300,
        bbox_inches="tight",
    )
    fig.savefig(
        output_dir / f"{name}.pdf",
        bbox_inches="tight",
    )
    plt.close(fig)


def plot_certified_quality(summary, output_dir):
    figure_topologies = (
        "sparse_random",
        "power_law",
        "fully_connected",
    )

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(13.2, 4.2),
        sharey=True,
    )

    for ax, graph_type in zip(axes, figure_topologies):
        sub = summary[summary["graph_type"] == graph_type]

        for strategy in ("S1", "S2"):
            line = sub[sub["strategy"] == strategy].sort_values("N")

            ax.errorbar(
                line["N"],
                line["mean"],
                yerr=line["ci95"],
                marker="o",
                capsize=3,
                label=strategy,
            )

        if graph_type == "fully_connected":
            ax.set_title("Fully Connected")

            ax.text(
                0.5,
                0.86,
                r"$S_1=S_2=\mathrm{LP}$",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=10,
            )
        else:
            ax.set_title(
                TOPOLOGY_LABELS[graph_type]
            )

        ax.set_xlabel(
            r"Number of parties $N$"
        )

        ax.set_xticks(N_VALUES)

        ax.set_ylim(
            0.0,
            1.05
        )

        ax.grid(
            alpha=0.25
        )

    axes[0].set_ylabel(
        r"Certified quality lower bound $S/\mathrm{LP}$"
    )

    axes[-1].legend()

    fig.suptitle(
        rf"Certified heuristic quality at $m={MAIN_QUALITY_M}$"
    )

    fig.tight_layout()

    save_figure(
        fig,
        output_dir,
        "figure1_certified_quality",
    )


def plot_feasibility(summary, output_dir):
    # Single-column manuscript layout: use 4 rows (p_del) x 3 columns (rho).
    # Row labels are placed INSIDE the first-column panels to avoid collisions
    # with the shared y-axis label after typesetting/resizing.
    fig, axes = plt.subplots(
        len(P_DEL_VALUES),
        len(RHO_VALUES),
        figsize=(9.6, 11.0),
        sharex=True,
        sharey=True,
    )

    for i, p_del in enumerate(P_DEL_VALUES):
        for j, rho in enumerate(RHO_VALUES):
            ax = axes[i, j]
            sub = summary[
                np.isclose(summary["rho"], rho)
                & np.isclose(summary["p_del"], p_del)
            ].copy()

            for m in M_VALUES:
                line = sub[sub["m"] == m].sort_values("N")

                ax.plot(
                    line["N"],
                    line["positive_LP_rate"],
                    marker="o",
                    linewidth=2.0,
                    markersize=5.2,
                    label=rf"$m={m}$",
                )

                # Annotate only clearly nontrivial points.
                for row in line.itertuples():
                    if row.positive_LP_rate < 0.95 - TOL:
                        y_offset = 7 if row.positive_LP_rate <= 0.5 else -13
                        ax.annotate(
                            f"{100.0 * row.positive_LP_rate:.0f}%",
                            (row.N, row.positive_LP_rate),
                            textcoords="offset points",
                            xytext=(0, y_offset),
                            ha="center",
                            fontsize=9.0,
                        )

            if i == 0:
                ax.set_title(
                    rf"$\rho={rho:.1f}$",
                    fontsize=12.5,
                    pad=6,
                )

            # Horizontal row label inside the leftmost panel.
            if j == 0:
                ax.text(
                    0.03,
                    0.08,
                    rf"$p_{{\rm del}}={p_del:g}$",
                    transform=ax.transAxes,
                    ha="left",
                    va="bottom",
                    fontsize=10.5,
                    fontweight="bold",
                    bbox=dict(
                        boxstyle="round,pad=0.2",
                        facecolor="white",
                        edgecolor="0.8",
                        alpha=0.9,
                    ),
                )

            ax.set_xticks(N_VALUES)
            ax.set_ylim(-0.03, 1.05)
            ax.set_yticks(np.linspace(0.0, 1.0, 6))
            ax.tick_params(axis="both", labelsize=9.5)
            ax.grid(alpha=0.22)

    fig.supxlabel(
        r"Number of parties $N$",
        fontsize=12.5,
        y=0.045,
    )
    fig.supylabel(
        r"Fraction of instances with $\mathrm{LP}>0$",
        fontsize=12.5,
        x=0.025,
    )

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        title="Memories per party",
        ncol=3,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.972),
        frameon=True,
        fontsize=10.0,
        title_fontsize=10.0,
    )

    fig.suptitle(
        "Sparse Random feasibility across density and memory loss",
        fontsize=15.0,
        y=0.992,
    )

    fig.subplots_adjust(
        left=0.105,
        right=0.985,
        bottom=0.085,
        top=0.875,
        hspace=0.18,
        wspace=0.10,
    )

    save_figure(
        fig,
        output_dir,
        "figure2_sparse_random_feasibility",
    )

def plot_matching_yield(summary, output_dir):
    fig, axes = plt.subplots(
        1,
        3,
        figsize=(14, 4.2),
        sharey=True,
    )

    for ax, graph_type in zip(axes, ALL_TOPOLOGIES):
        sub = summary[summary["graph_type"] == graph_type]

        for strategy in ("S1", "S2"):
            line = sub[sub["strategy"] == strategy].sort_values("p_del")

            ax.errorbar(
                line["p_del"],
                line["mean"],
                yerr=line["ci95"],
                marker="o",
                capsize=3,
                label=strategy,
            )

        ax.set_title(TOPOLOGY_LABELS[graph_type])
        ax.set_xlabel(r"Memory-loss probability $p_{\rm del}$")
        ax.set_xticks(P_DEL_VALUES)
        ax.set_ylim(0.0, 1.05)
        ax.grid(alpha=0.25)

    axes[0].set_ylabel(r"Normalized matching yield $S/m$")
    axes[-1].legend()

    fig.suptitle("Matching yield under memory loss")
    fig.tight_layout()

    save_figure(
        fig,
        output_dir,
        "figure3_matching_yield",
    )


def cell_median_by_N_m(data, value_col):
    data = data[data[value_col].notna()].copy()
    data = data[data[value_col] > 0].copy()

    summary = (
        data.groupby(
            ["graph_type", "N", "m", "total_nodes"],
            dropna=False,
        )[value_col]
        .median()
        .reset_index(name="cell_median")
    )
    return summary


def aggregate_cell_medians_by_size(cell_summary):
    # Different (N, m) cells can have the same Nm. First compute the median in
    # each (N, m) cell, then take the median of those cell medians so every
    # configuration receives equal weight.
    return (
        cell_summary.groupby(
            ["graph_type", "total_nodes"],
            dropna=False,
        )["cell_median"]
        .median()
        .reset_index(name="median")
    )


def plot_runtime_line(ax, summary, graph_type, x_col, label=None):
    line = summary[
        summary["graph_type"] == graph_type
    ].sort_values(x_col)

    if len(line) == 0:
        return

    if label is None:
        label = TOPOLOGY_LABELS[graph_type]

    ax.plot(
        line[x_col],
        line["median"],
        marker="o",
        label=label,
    )


def plot_runtime_scaling(df, output_dir):
    # The paper compares the two routing heuristics. The LP is used only as a
    # reference upper bound, so it is intentionally excluded from this figure.
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(10, 4.2),
        sharey=True,
    )

    # Strategy 1
    s1_cells = cell_median_by_N_m(
        data=df,
        value_col="runtime_S1",
    )
    s1_summary = aggregate_cell_medians_by_size(s1_cells)

    for graph_type in ALL_TOPOLOGIES:
        plot_runtime_line(
            ax=axes[0],
            summary=s1_summary,
            graph_type=graph_type,
            x_col="total_nodes",
        )

    axes[0].set_title("Strategy 1")
    axes[0].set_xlabel(r"Total memory nodes $Nm$")
    axes[0].set_ylabel("Median runtime (seconds)")
    axes[0].legend(loc="upper left", fontsize=8)

    # Strategy 2
    s2_cells = cell_median_by_N_m(
        data=df,
        value_col="runtime_S2",
    )
    s2_summary = aggregate_cell_medians_by_size(s2_cells)

    for graph_type in ALL_TOPOLOGIES:
        plot_runtime_line(
            ax=axes[1],
            summary=s2_summary,
            graph_type=graph_type,
            x_col="total_nodes",
        )

    axes[1].set_title("Strategy 2")
    axes[1].set_xlabel(r"Total memory nodes $Nm$")
    axes[1].legend(loc="upper left", fontsize=8)

    for ax in axes:
        ax.set_yscale("log")
        ax.grid(alpha=0.25)

    fig.suptitle("Runtime scaling")
    fig.tight_layout()

    save_figure(
        fig,
        output_dir,
        "figure4_runtime_scaling",
    )


def print_key_results(df, quality_main, feasibility_main):
    print("\nKey descriptive results:")

    print(
        f"\nCertified quality lower bounds at m={MAIN_QUALITY_M} "
        "(conditional on LP > 0):"
    )
    quality_table = quality_main.pivot_table(
        index=["graph_type", "N"],
        columns="strategy",
        values="mean",
    )
    print(quality_table.to_string())

    print(
        "\nSparse Random positive-LP fraction "
        "across rho, p_del, N, and m:"
    )
    feasibility_table = feasibility_main.pivot_table(
        index=["rho", "p_del", "N"],
        columns="m",
        values="positive_LP_rate",
    )
    print(feasibility_table.to_string())

    win_rates = (
        df.groupby("graph_type")["winner"]
        .value_counts(normalize=True)
        .unstack(fill_value=0)
    )

    print("\nOverall S1/S2 win rates:")
    print(win_rates.to_string())

    sparse_only = df[
        df["graph_type"].isin(SPARSE_TOPOLOGIES)
    ].copy()
    sparse_only["S1_not_worse"] = (
        sparse_only["S1"] >= sparse_only["S2"]
    )

    not_worse = sparse_only.groupby(
        "graph_type"
    )["S1_not_worse"].mean()

    print("\nS1 not-worse-than-S2 rate:")
    print(not_worse.to_string())

    zero_lp_by_N = (
        sparse_only.assign(zero_LP=sparse_only["LP_upper_bound"] <= TOL)
        .groupby(["graph_type", "N"])["zero_LP"]
        .mean()
    )
    print("\nOverall zero-LP rate by topology and N:")
    print(zero_lp_by_N.to_string())


def main():
    args = parse_args()

    input_path = resolve_input_path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(f"Reading: {input_path}")

    df = pd.read_csv(input_path)
    validate_columns(df)
    df = add_derived_columns(df)

    print(f"Rows: {len(df)}")
    print("\nRows by topology:")
    print(df["graph_type"].value_counts().to_string())

    write_sanity_report(
        df=df,
        output_dir=output_dir,
    )
    save_parameter_coverage(
        df=df,
        output_dir=output_dir,
    )

    quality_detailed, quality_main = create_certified_quality_summary(
        df=df,
        output_dir=output_dir,
    )
    feasibility_detailed, feasibility_main = create_feasibility_summary(
        df=df,
        output_dir=output_dir,
    )
    yield_summary = create_yield_summary(
        df=df,
        output_dir=output_dir,
    )

    save_win_rate_tables(
        df=df,
        output_dir=output_dir,
    )
    save_density_summaries(
        df=df,
        output_dir=output_dir,
    )
    save_runtime_summary(
        df=df,
        output_dir=output_dir,
    )

    plot_certified_quality(
        summary=quality_main,
        output_dir=output_dir,
    )
    plot_feasibility(
        summary=feasibility_main,
        output_dir=output_dir,
    )
    plot_matching_yield(
        summary=yield_summary,
        output_dir=output_dir,
    )
    plot_runtime_scaling(
        df=df,
        output_dir=output_dir,
    )

    print_key_results(
        df=df,
        quality_main=quality_main,
        feasibility_main=feasibility_main,
    )

    print("\nAnalysis complete.")
    print("\nMain figures:")
    print("  figure1_certified_quality")
    print("  figure2_sparse_random_feasibility")
    print("  figure3_matching_yield")
    print("  figure4_runtime_scaling")
    print(f"\nOutputs saved to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
