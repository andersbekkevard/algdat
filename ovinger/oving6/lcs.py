def lcs(s1, s2, visualize=False):
    n = len(s1)
    m = len(s2)
    table = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])

    if visualize:
        visualize_lcs_table(table, s1, s2)

    return table[n][m]


def visualize_lcs_table(table, s1, s2):
    """
    Visualize the LCS dynamic programming table using matplotlib.
    Shows values, arrows indicating the path, and labeled strings.
    Uses heatmap coloring to show value progression.
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyArrowPatch
    from matplotlib.colors import LinearSegmentedColormap
    import numpy as np

    n = len(s1)
    m = len(s2)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(max(10, m + 2), max(8, n + 2)))
    ax.set_xlim(-0.5, m + 1.5)
    ax.set_ylim(-0.5, n + 1.5)
    ax.set_aspect("equal")
    ax.invert_yaxis()

    # Find max value for color normalization
    max_value = max(max(row) for row in table)

    # Create custom colormap (white -> light blue -> blue)
    colors = ["#ffffff", "#e3f2fd", "#90caf9", "#42a5f5", "#1e88e5", "#1565c0"]
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list("lcs_heatmap", colors, N=n_bins)

    # Draw grid
    for i in range(n + 2):
        for j in range(m + 2):
            # Add values from table with heatmap coloring
            if i <= n and j <= m:
                value = table[i][j]

                # Calculate color based on value
                if max_value > 0:
                    color_intensity = value / max_value
                    cell_color = cmap(color_intensity)
                else:
                    cell_color = "white"

                # Draw cell with heatmap color
                rect = patches.Rectangle(
                    (j - 0.5, i - 0.5),
                    1,
                    1,
                    linewidth=1.5,
                    edgecolor="black",
                    facecolor=cell_color,
                )
                ax.add_patch(rect)

                # Choose text color based on background intensity
                text_color = "#2c3e50" if color_intensity < 0.5 else "white"

                ax.text(
                    j,
                    i,
                    str(value),
                    ha="center",
                    va="center",
                    fontsize=14,
                    fontweight="bold",
                    color=text_color,
                )
            else:
                # Draw empty cell for labels area
                rect = patches.Rectangle(
                    (j - 0.5, i - 0.5),
                    1,
                    1,
                    linewidth=1.5,
                    edgecolor="black",
                    facecolor="white",
                )
                ax.add_patch(rect)

    # Add column labels (s2) at the top
    ax.text(-0.5, -0.5, "j", ha="center", va="center", fontsize=12, style="italic")
    for j in range(m + 1):
        ax.text(
            j,
            -0.5,
            str(j),
            ha="center",
            va="center",
            fontsize=11,
            color="#c0392b",
            fontweight="bold",
        )

    # Add row labels (s1) on the left
    ax.text(-0.5, -0.5, "i", ha="center", va="center", fontsize=12, style="italic")
    for i in range(n + 1):
        ax.text(
            -0.5,
            i,
            str(i),
            ha="center",
            va="center",
            fontsize=11,
            color="#c0392b",
            fontweight="bold",
        )

    # Add string characters on the right side (s1)
    for i, char in enumerate(s1):
        rect = patches.Rectangle(
            (m + 0.5, i + 0.5),
            1,
            1,
            linewidth=1.5,
            edgecolor="black",
            facecolor="#95a5a6",
        )
        ax.add_patch(rect)
        ax.text(
            m + 1,
            i + 1,
            char,
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            color="white",
        )

    # Add string characters on the bottom (s2)
    for j, char in enumerate(s2):
        rect = patches.Rectangle(
            (j + 0.5, n + 0.5),
            1,
            1,
            linewidth=1.5,
            edgecolor="black",
            facecolor="#34495e",
        )
        ax.add_patch(rect)
        ax.text(
            j + 1,
            n + 1,
            char,
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            color="white",
        )

    # Add arrows showing the direction decisions
    arrow_props = dict(arrowstyle="<-", lw=1.5, color="#3498db")

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Determine arrow direction based on how value was computed
            if s1[i - 1] == s2[j - 1]:
                # Diagonal arrow (match)
                arrow = FancyArrowPatch(
                    (j - 0.3, i - 0.3),
                    (j - 0.15, i - 0.15),
                    arrowstyle="<-",
                    lw=2,
                    color="#27ae60",
                    mutation_scale=15,
                )
                ax.add_patch(arrow)
            else:
                # Check which direction contributed to max
                if table[i - 1][j] > table[i][j - 1]:
                    # Up arrow
                    arrow = FancyArrowPatch(
                        (j, i - 0.35),
                        (j, i - 0.15),
                        arrowstyle="<-",
                        lw=1.5,
                        color="#3498db",
                        mutation_scale=12,
                    )
                    ax.add_patch(arrow)
                elif table[i - 1][j] < table[i][j - 1]:
                    # Left arrow
                    arrow = FancyArrowPatch(
                        (j - 0.35, i),
                        (j - 0.15, i),
                        arrowstyle="<-",
                        lw=1.5,
                        color="#3498db",
                        mutation_scale=12,
                    )
                    ax.add_patch(arrow)
                else:
                    # Both equal - show up arrow (arbitrary choice)
                    arrow = FancyArrowPatch(
                        (j, i - 0.35),
                        (j, i - 0.15),
                        arrowstyle="<-",
                        lw=1.5,
                        color="#95a5a6",
                        mutation_scale=12,
                    )
                    ax.add_patch(arrow)

    # Labels and title
    ax.text(
        m / 2,
        -1.2,
        f'LCS Table: "{s1}" vs "{s2}"',
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
    )
    ax.text(
        m / 2,
        n + 2.2,
        f"Longest Common Subsequence Length: {table[n][m]}",
        ha="center",
        va="center",
        fontsize=14,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#3498db", alpha=0.3),
    )

    # Legend
    legend_x = m + 0.5
    legend_y = -0.5
    ax.text(legend_x, legend_y, "Legend:", fontsize=10, fontweight="bold")
    ax.text(legend_x, legend_y + 0.3, "→ Diagonal: Match", fontsize=9, color="#27ae60")
    ax.text(
        legend_x, legend_y + 0.6, "→ Up/Left: No match", fontsize=9, color="#3498db"
    )

    # Add colorbar to show value scale
    import matplotlib.cm as cm
    from matplotlib.colorbar import ColorbarBase
    from matplotlib.colors import Normalize

    # Create a separate axis for colorbar
    cbar_ax = fig.add_axes([0.92, 0.3, 0.02, 0.4])  # [left, bottom, width, height]
    norm = Normalize(vmin=0, vmax=max_value)
    cb = ColorbarBase(cbar_ax, cmap=cmap, norm=norm, orientation="vertical")
    cb.set_label("LCS Value", rotation=270, labelpad=20, fontsize=11, fontweight="bold")
    cb.ax.tick_params(labelsize=9)

    ax.axis("off")
    plt.tight_layout()
    plt.show()


# Test the function
print(f"LCS length: {lcs('signatur', 'skigard', visualize=True)}")
