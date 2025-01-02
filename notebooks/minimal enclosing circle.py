import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md("# Problem")
    return


@app.cell
def _(mo):
    mo.md(
        "We compute the radius and center of the smallest enclosing ball for $N$ points in $d$ dimensions. We use a variety of tools and compare their performance."
    )
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("## Generate a cloud of points")
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
    mo.md("## Compute with cvxpy")
    return


@app.cell
def _(np):
    import cvxpy as cp

    # We compare 3 equivalent ways to create the constraint that
    # each point has to be within the ball of radius r centered at x
    def con_1(points, x, r):
        return [cp.norm(point - x) <= r for point in points]

    def con_2(points, x, r):
        return [cp.SOC(r, point - x) for point in points]

    def con_3(points, x, r):
        return [
            cp.SOC(
                r * np.ones(points.shape[0]),
                points - cp.outer(np.ones(points.shape[0]), x),
                axis=1,
            )
        ]

    def min_circle_cvx(points, fct=None, **kwargs):
        # Use con_1 if no constraint construction is defined
        fct = fct or con_1
        # cvxpy variable for the radius
        r = cp.Variable(1, name="Radius")
        # cvxpy variable for the midpoint
        x = cp.Variable(points.shape[1], name="Midpoint")

        objective = cp.Minimize(r)
        constraints = fct(points, x, r)

        problem = cp.Problem(objective=objective, constraints=constraints)
        problem.solve(**kwargs)

        return {"Radius": r.value, "Midpoint": x.value}

    return con_1, con_2, con_3, cp, min_circle_cvx


@app.cell
def _(con_1, min_circle_cvx, pos):
    min_circle_cvx(points=pos, fct=con_1, solver="CLARABEL")
    return


@app.cell
def _(con_2, min_circle_cvx, pos):
    min_circle_cvx(points=pos, fct=con_2, solver="CLARABEL")
    return


@app.cell
def _(con_3, min_circle_cvx, pos):
    min_circle_cvx(points=pos, fct=con_3, solver="CLARABEL")
    return


@app.cell
def _(con_3, min_circle_cvx, pos):
    # CLARABEL is the only option :-)
    min_circle_cvx(points=pos, fct=con_3)
    return


if __name__ == "__main__":
    app.run()
