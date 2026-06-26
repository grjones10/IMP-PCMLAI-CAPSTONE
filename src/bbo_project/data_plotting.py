import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


from scipy.spatial import ConvexHull

# =========================================================
# Helper: Axis formatting
# =========================================================
def style_axis(ax, limits, ticks, labels=False):
    ax.set_axisbelow(True)
    ax.set_xlim(*limits)
    ax.set_ylim(*limits)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", linewidth=0.8, color="lightgrey")

    if labels is False:
        ax.set_xlabel("")
        ax.set_ylabel("")

def domain_plot(folder_name, 
                save_path,
                x_cols, 
                points, 
                points_hull,
                flag = None,
                hull = None,
                contour = None,
                bounds = None,
                next_point = None,
                limits=(-0.1, 1.1),
                ticks=(0.0, 0.5, 1.0)
):

    n = len(x_cols)
    fig, axes = plt.subplots(n, n, figsize=(2.5*n, 2.5*n))

    if n == 1:
        axes = np.array([[axes]])

    for i in range(n):
        for j in range(n):
            ax = axes[i][j]

            if i == j:
                ax.text(0.5, 0.5, x_cols[i], ha="center", va="center", fontsize=16)
                ax.set_xticks([])
                ax.set_yticks([])
                for spine in ax.spines.values():
                    spine.set_visible(False)
                continue
            # ---------------------------
            # Extract 2D projection
            # ---------------------------
            x = points[:, j]
            y = points[:, i]


            # ---------------------------
            # Plot points
            # ---------------------------

            cmap = ListedColormap(["mistyrose", "darkred"])

            if flag is not None:
                ax.scatter(
                    x, 
                    y,
                    c = flag, 
                    cmap=cmap,
                    vmin=0, 
                    vmax=1,
                    edgecolor="darkred",
                    linewidth=1,
                    s=16,
                    zorder=8,
                    )
            
            else:
                ax.scatter(
                    x, 
                    y,
                    color = "mistyrose", 
                    edgecolor="darkred",
                    linewidth=1,
                    s=16,
                    zorder=8,
                    )

            # ---------------------------
            # Plot convex hull (2D projection)
            # ---------------------------
            if hull is not None:
                plot_2d_hull(ax, hull, points_hull, i, j)

            if contour is not None:
                plt.suptitle(f"Output Contours ({folder_name})", fontsize=16)

                grid_res = 50

                from scipy.interpolate import griddata

                Y_scaled = (y - y.min()) / (y.max() - y.min() + 1e-12)

                grid_x = np.linspace(limits[0], limits[1], grid_res)
                grid_y = np.linspace(limits[0], limits[1], grid_res)
                XX, YY = np.meshgrid(grid_x, grid_y)

                grid_points = np.column_stack((x, y))
                ZZ = griddata(grid_points, contour, (XX, YY), method="linear")

                ax.contourf(
                    XX, YY, ZZ,
                    levels=np.linspace(0, 1, 32),
                    cmap="viridis",
                    alpha=0.5,
                    vmin = 0,
                    vmax = 1,
                    zorder=0
                )
                # add_contours(x_cols, y, axes, limits=limits)
            # ---------------------------
            # Calculated next point
            # ---------------------------
            if next_point is not None:

                # plot_bounds(ax, bounds_info, X_cols, i, j)

                ax.scatter(
                    next_point[x_cols[j]],
                    next_point[x_cols[i]],
                    color="plum",
                    edgecolor="darkviolet",
                    linewidth=1,
                    s=22,
                    zorder=8,
                )


            # ---------------------------
            # Styling
            # ---------------------------
            style_axis(ax, limits, ticks)

    if contour is None:
        plt.suptitle(f"Input Domain Plot ({folder_name})", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    if save_path is not None:
        if contour is not None:
            save_filename = save_path / "domain_scatter_contour.png"
        else:
            save_filename = save_path / "domain_scatter.png"
            
        plt.savefig(save_filename, dpi=300)

def plot_2d_hull(ax, hull, points, i, j, color="lightgrey"):
    """
    Project a high-dimensional convex hull into 2D (dims j vs i)
    and draw it on the given axis.
    
    Parameters
    ----------
    ax : matplotlib axis
    hull : scipy.spatial.ConvexHull
    points : ndarray (n_samples, n_dims)
    i, j : int
        Indices of the dimensions to plot (y=i, x=j)
    """

    if hull is None:
        return

    # Extract hull vertices
    hull_points = points[hull.vertices]

    # Project to 2D
    proj = hull_points[:, [j, i]]

    # Need at least 3 points for a hull
    if proj.shape[0] < 3:
        return

    try:
        hull_2d = ConvexHull(proj)

        # Draw edges
        for simplex in hull_2d.simplices:
                    
            ax.fill(
                proj[hull_2d.vertices, 0],
                proj[hull_2d.vertices, 1],
                color=color,
                alpha=0.1,
                zorder=0,
                edgecolor = None
            )
    except Exception:
        # In case projection is degenerate (collinear, etc.)
        pass

# =========================================================
# OUTPUT VS INPUTS
# =========================================================

import numpy as np
from matplotlib.colors import ListedColormap

def domain_io_plot(
    folder_name,
    save_path,
    x_cols,
    y_cols,
    X,
    Y,
    Z=None,
    next_point=None,
    limits=(-0.1, 1.1),
    ticks=(0.0, 0.5, 1.0),
):
    """
    Grid of outputs (rows) vs inputs (columns)
    """

    n_in = len(x_cols)
    n_out = len(y_cols)

    fig, axes = plt.subplots(
        n_out, n_in,
        figsize=(2.5 * n_in, 2.5 * n_out)
    )

    if n_out == 1:
        axes = np.array([axes])
    if n_in == 1:
        axes = np.array([[ax] for ax in axes])


    for i in range(n_out):      # output index (rows)
        for j in range(n_in):   # input index (cols)

            ax = axes[i][j]

            x = X[:, j]
            y = Y[:, i]

            # ---------------------------
            # Scatter: input → output
            # ---------------------------
            cmap = ListedColormap(["lightgrey", "indianred"])

            if Z is not None:
                ax.scatter(
                    x,
                    y,
                    c=Z,
                    cmap=cmap,
                    vmin=0,
                    vmax=1,
                    edgecolor="darkred",
                    linewidth=1,
                    s=14,
                    zorder=8,
                )
            else:
                ax.scatter(
                    x,
                    y,
                    color="mistyrose",
                    edgecolor="darkred",
                    linewidth=1,
                    s=14,
                    zorder=8,
                )

            # ---------------------------
            # Next point (projection)
            # ---------------------------
            if next_point is not None:
                ax.axvline(
                    next_point[x_cols[j]],
                    color="darkviolet",
                    linewidth=1.5,
                    linestyle='--',
                    zorder=6,
                )

            # ---------------------------
            # Labels
            # ---------------------------
            if i == n_out - 1:
                ax.set_xlabel(x_cols[j])
            else:
                ax.set_xticklabels([])

            if j == 0:
                ax.set_ylabel(y_cols[i])
            else:
                ax.set_yticklabels([])

            # ---------------------------
            # Styling
            # ---------------------------
            style_axis(ax, limits, ticks, labels=True)

    plt.suptitle(f"Input → Output Plot ({folder_name})", fontsize=16)
    plt.tight_layout()

    if save_path is not None:
        save_filename = save_path / "io_scatter.png"
        plt.savefig(save_filename, dpi=300)

    return fig, axes

# # =========================================================
# # CONTOURS
# # =========================================================
# def add_contours(X_cols, Y, axes, limits=(-0.2, 1.2), grid_res=50, cmap="viridis"):

#     from scipy.interpolate import griddata

#     # X_cols = get_X_cols(df)
#     # Y = df["Y1"].values

#     # Normalize
#     Y_scaled = (Y - Y.min()) / (Y.max() - Y.min() + 1e-12)

#     grid_x = np.linspace(limits[0], limits[1], grid_res)
#     grid_y = np.linspace(limits[0], limits[1], grid_res)
#     XX, YY = np.meshgrid(grid_x, grid_y)

#     n = len(X_cols)

#     for i in range(n):
#         for j in range(n):
#             if i == j:
#                 continue

#             ax = axes[i][j]

#             x = df[X_cols[j]].values
#             y = df[X_cols[i]].values

#             points = np.column_stack((x, y))
#             ZZ = griddata(points, Y_scaled, (XX, YY), method="linear")

#             ax.contourf(
#                 XX, YY, ZZ,
#                 levels=np.linspace(0, 1, 16),
#                 cmap=cmap,
#                 alpha=0.4,
#                 zorder=0
#             )



def plot_hyperparameter_surface(svm_cross_validation, save_path):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.ndimage import gaussian_filter

    # ----------------------------
    # 1. Pivot table (raw grid)
    # ----------------------------
    pivot = svm_cross_validation.pivot(
        index="C",
        columns="gamma",
        values="Accuracy"
    )

    C_vals = pivot.index.values.astype(float)
    gamma_vals = pivot.columns.values.astype(float)

    # ----------------------------
    # 2. Smooth directly on raw grid
    # ----------------------------
    smoothed_array = gaussian_filter(pivot.values, sigma=1.5)

    smoothed = pd.DataFrame(
        smoothed_array,
        index=C_vals,
        columns=gamma_vals
    )

    # ----------------------------
    # 3. Find maximum
    # ----------------------------
    max_idx = np.unravel_index(
        np.argmax(smoothed.values),
        smoothed.values.shape
    )

    C_max = smoothed.index[max_idx[0]]
    gamma_max = smoothed.columns[max_idx[1]]
    max_val = smoothed.values[max_idx]

    # ----------------------------
    # 4. Plot
    # ----------------------------
    plt.figure(figsize=(6, 5))

    plt.imshow(
        smoothed.values,
        origin="lower",
        aspect="auto",
        cmap="Spectral_r",
        vmin=0.75,
        vmax=1
    )

    plt.colorbar(label="Smoothed Accuracy")

    plt.xlabel("gamma")
    plt.ylabel("C")
    plt.title("Hyperparameter Surface")

    # ----------------------------
    # 5. Tick control (every N steps)
    # ----------------------------
    step = 4  # adjust density here

    x_pos = np.arange(0, len(gamma_vals), step)
    y_pos = np.arange(0, len(C_vals), step)

    plt.xticks(
        x_pos,
        [f"{gamma_vals[i]:.2g}" for i in x_pos],
        rotation=0
    )

    plt.yticks(
        y_pos,
        [f"{C_vals[i]:.2g}" for i in y_pos]
    )

    # ----------------------------
    # 6. Mark maximum
    # ----------------------------
    plt.scatter(
        max_idx[1],
        max_idx[0],
        color="black",
        s=80,
        zorder=10,
        label=f"C={C_max:.1f}, gamma={gamma_max:.1f}"
    )

    plt.legend()
    plt.tight_layout()

    # Save BEFORE show
    save_filename = save_path / "svm_hyperparameter_surface.png"
    plt.savefig(save_filename, dpi=300)

    plt.show()

    return C_max, gamma_max, max_val