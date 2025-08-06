# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.13.15",
#     "clarabel==0.11.0",
#     "cvxpy-base==1.6.6",
#     "plotly==6.1.2",
#     "numpy==2.3.0",
# ]
# ///
"""Minimal enclosing circle computation for a set of points in multiple dimensions.

This notebook demonstrates different methods to compute the smallest enclosing ball
for a set of points, using CVXPY as the optimization tool.
"""

import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")

with app.setup:
    import cvxpy as cp
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go


@app.cell
def _():
    mo.md(
        """
    # Problem

    We compute the radius and center of the smallest enclosing ball for $N$ points in $d$ dimensions.
    We use a variety of tools and compare their performance.
    """
    )
    return


@app.cell
def _():
    mo.md("""## Generate a cloud of points""")
    return


@app.cell
def _():
    rng = np.random.default_rng()
    pos = rng.standard_normal((1000, 11))
    return (pos,)


@app.cell
def _(pos):
    # Create the scatter plot
    fig = go.Figure(data=go.Scatter(x=pos[:, 0], y=pos[:, 1], mode="markers", marker={"symbol": "x", "size": 10}))

    # Update layout for equal aspect ratio and axis labels
    fig.update_layout(
        xaxis_title="x",
        yaxis_title="y",
        yaxis={
            "scaleanchor": "x",
            "scaleratio": 1,
        },
    )

    # Show the plot
    fig

    # plot makes really only sense when using d=2
    return


@app.cell
def _():
    mo.md("""## Compute with cvxpy""")
    return


@app.function
def min_circle_cvx(points, **kwargs):
    """Compute the minimum enclosing circle using CVXPY.

    Args:
        points: A numpy array of shape (n, d) containing n points in d dimensions.
        **kwargs: Additional arguments to pass to the CVXPY solver.

    Returns:
        dict: A dictionary containing the radius and midpoint of the minimum enclosing circle.
    """
    # cvxpy variable for the radius
    r = cp.Variable(1, name="Radius")
    # cvxpy variable for the midpoint
    x = cp.Variable(points.shape[1], name="Midpoint")

    objective = cp.Minimize(r)
    constraints = [
        cp.SOC(
            r * np.ones(points.shape[0]),
            points - cp.outer(np.ones(points.shape[0]), x),
            axis=1,
        )
    ]

    problem = cp.Problem(objective=objective, constraints=constraints)
    problem.solve(**kwargs)

    return {"Radius": r.value, "Midpoint": x.value}


@app.cell
def _(pos):
    min_circle_cvx(points=pos, solver="CLARABEL")
    return


if __name__ == "__main__":
    app.run()
