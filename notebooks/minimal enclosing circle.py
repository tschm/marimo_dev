import marimo

__generated_with = "0.10.15"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md("""# Problem""")
    return


@app.cell
def _(mo):
    mo.md("""We compute the radius and center of the smallest enclosing ball for $N$ points in $d$ dimensions. We use a variety of tools and compare their performance.""")
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md("""## Generate a cloud of points""")
    return


@app.cell
def _():
    import plotly.graph_objects as go
    import numpy as np
    return go, np


@app.cell
def _(np):
    pos = np.random.randn(1000, 11)
    return (pos,)


@app.cell
def _(go, pos):
    # Create the scatter plot
    fig = go.Figure(
        data=go.Scatter(
            x=pos[:, 0], y=pos[:, 1], mode="markers", marker=dict(symbol="x", size=10)
        )
    )

    # Update layout for equal aspect ratio and axis labels
    fig.update_layout(
        xaxis_title="x",
        yaxis_title="y",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
        ),
    )

    # Show the plot
    fig.show()

    # plot makes really only sense when using d=2
    return (fig,)


@app.cell
def _(mo):
    mo.md("""## Compute with cvxpy""")
    return


@app.cell
def _(np):
    import cvxpy as cp

    def min_circle_cvx(points, **kwargs):
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
    return cp, min_circle_cvx


@app.cell
def _(min_circle_cvx, pos):
    min_circle_cvx(points=pos, solver="CLARABEL")
    return


if __name__ == "__main__":
    app.run()
