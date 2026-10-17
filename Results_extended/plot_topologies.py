import random
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# =========================================================
# Basic settings
# =========================================================

M = 5                  # memories per party shown in the schematic
NUM_PEERS = 3          # P1, P2, P3
EDGES_PER_PEER = 8     # same edge budget for sparse random and power-law
SEED = 31

OUTPUT_DIR = Path("")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PNG = OUTPUT_DIR / "router_topologies.png"
OUTPUT_PDF = OUTPUT_DIR / "router_topologies.pdf"


# =========================================================
# Generate topologies
# =========================================================

def generate_sparse_random_edges():
    """
    Generate a representative Sparse Random topology.
    Each center-peer layer contains exactly EDGES_PER_PEER edges.
    """
    for seed in range(SEED, SEED + 500):
        rng = random.Random(seed)

        edges = []
        layer_degrees = []

        for p in range(1, NUM_PEERS + 1):
            possible_edges = [(c, j) for c in range(M) for j in range(M)]
            chosen = rng.sample(possible_edges, EDGES_PER_PEER)

            deg = [0] * M
            for c, j in chosen:
                edges.append((c, p, j))
                deg[c] += 1
            layer_degrees.append(deg)

        total_degrees = [
            sum(layer_degrees[p][c] for p in range(NUM_PEERS))
            for c in range(M)
        ]

        persistent_hub = any(
            all(layer_degrees[p][c] >= 3 for p in range(NUM_PEERS))
            for c in range(M)
        )

        max_layer_degree = max(max(row) for row in layer_degrees)

        if (
            not persistent_hub
            and max_layer_degree <= 3
            and max(total_degrees) - min(total_degrees) <= 5
            and all(d > 0 for d in total_degrees)
        ):
            return edges, layer_degrees, seed

    raise RuntimeError("Could not find a suitable Sparse Random example.")


def generate_power_law_edges():
    """
    Schematic Power-Law Center-Degree topology.
    The same center-degree sequence is reused in each layer.
    """
    rng = random.Random(SEED + 1000)

    center_degree_sequence = [5, 2, 1, 0, 0]   # sum = 8

    if sum(center_degree_sequence) != EDGES_PER_PEER:
        raise ValueError("Power-law edge budget must match sparse random budget.")

    edges = []

    for p in range(1, NUM_PEERS + 1):
        for c, degree in enumerate(center_degree_sequence):
            if degree == 0:
                continue
            peer_targets = rng.sample(range(M), degree)
            for j in peer_targets:
                edges.append((c, p, j))

    return edges, center_degree_sequence


def generate_fully_connected_edges():
    """
    Fully connected topology: every center memory is connected
    to every peer memory.
    """
    return [
        (c, p, j)
        for p in range(1, NUM_PEERS + 1)
        for c in range(M)
        for j in range(M)
    ]


# =========================================================
# Layout / positions
# =========================================================

def generate_positions():
    x_positions = {
        "C": 0.0,
        "P1": 2.2,
        "P2": 4.4,
        "P3": 6.6,
    }

    y_positions = [4.0, 3.0, 2.0, 1.0, 0.0]

    positions = {}

    for c in range(M):
        positions[("C", c)] = (x_positions["C"], y_positions[c])

    for p in range(1, NUM_PEERS + 1):
        for j in range(M):
            positions[(f"P{p}", j)] = (x_positions[f"P{p}"], y_positions[j])

    return positions


# =========================================================
# Draw one topology
# =========================================================

def draw_topology(ax, edges, panel_label):
    positions = generate_positions()

    # ---- edges ----
    for c, p, j in edges:
        x1, y1 = positions[("C", c)]
        x2, y2 = positions[(f"P{p}", j)]
        ax.plot(
            [x1, x2], [y1, y2],
            color="black",
            linewidth=0.65,
            alpha=0.9,
            zorder=1,
            solid_capstyle="round"
        )

    # ---- nodes ----
    radius = 0.25

    # Center nodes
    for c in range(M):
        x, y = positions[("C", c)]
        ax.add_patch(
            Circle(
                (x, y),
                radius,
                facecolor="white",
                edgecolor="black",
                linewidth=1.3,
                zorder=3
            )
        )
        ax.text(
            x, y,
            rf"$C^{{{c+1}}}$",
            ha="center",
            va="center",
            fontsize=13,
            zorder=4
        )

    # Peer nodes
    for p in range(1, NUM_PEERS + 1):
        for j in range(M):
            x, y = positions[(f"P{p}", j)]
            ax.add_patch(
                Circle(
                    (x, y),
                    radius,
                    facecolor="white",
                    edgecolor="black",
                    linewidth=1.3,
                    zorder=3
                )
            )
            ax.text(
                x, y,
                rf"$P_{{{p}}}^{{{j+1}}}$",
                ha="center",
                va="center",
                fontsize=11.5,
                zorder=4
            )

    # ---- column labels ----
    ax.text(0.0, 4.58, r"$C$", ha="center", va="bottom", fontsize=15)
    ax.text(2.2, 4.58, r"$P_1$", ha="center", va="bottom", fontsize=15)
    ax.text(4.4, 4.58, r"$P_2$", ha="center", va="bottom", fontsize=15)
    ax.text(6.6, 4.58, r"$P_3$", ha="center", va="bottom", fontsize=15)

    # ---- panel label below ----
    ax.text(
        0.5, -0.13,
        panel_label,
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=12.5
    )

    ax.set_aspect("equal")
    ax.set_xlim(-0.55, 7.15)
    ax.set_ylim(-0.55, 5.05)
    ax.axis("off")


# =========================================================
# Main
# =========================================================

def main():
    sparse_edges, sparse_degrees, sparse_seed = generate_sparse_random_edges()
    power_edges, power_degrees = generate_power_law_edges()
    full_edges = generate_fully_connected_edges()

    # Font settings: slightly larger
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "font.size": 13
    })

    # Horizontal 1x3 layout
    fig, axes = plt.subplots(1, 3, figsize=(16, 5.6))

    draw_topology(axes[0], sparse_edges, "(a) Sparse Random")
    draw_topology(axes[1], power_edges, "(b) Power-Law Center-Degree")
    draw_topology(axes[2], full_edges, "(c) Fully Connected")

    fig.subplots_adjust(
        left=0.03,
        right=0.995,
        top=0.97,
        bottom=0.19,
        wspace=0.12
    )

    fig.savefig(
        OUTPUT_PNG,
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )
    fig.savefig(
        OUTPUT_PDF,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.show()

    print("\nSparse Random center degrees:")
    for i, row in enumerate(sparse_degrees, start=1):
        print(f"P{i}: {row}")

    print("\nPower-Law center degree sequence:")
    print(power_degrees)

    print(f"\nSame edge budget per peer layer: {EDGES_PER_PEER}")
    print(f"Sparse Random seed: {sparse_seed}")
    print(f"\nPNG saved to: {OUTPUT_PNG}")
    print(f"PDF saved to: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
