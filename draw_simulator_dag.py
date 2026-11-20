
from functools import partialmethod
from pathlib import Path
import daft


class dag(daft.PGM):
    def __init__(self, *args, **kwargs):
        daft.PGM.__init__(self, *args, **kwargs)

    latNode = partialmethod(
        daft.PGM.add_node,
        scale=1.3,
        aspect=2.4,
        fontsize=10,
        plot_params={"facecolor": "aliceblue"}
    )

    detNode = partialmethod(
        daft.PGM.add_node,
        aspect=5.4,
        fontsize=9.25,
        alternate=True,
        plot_params={"facecolor": "aliceblue"}
    )

    decNode = partialmethod(
        daft.PGM.add_node,
        scale=1.3,
        aspect=2.4,
        fontsize=10,
        shape="rectangle",
        plot_params={"facecolor": "lightyellow"}
    )


pgm = dag(dpi=150, alternate_style="outer")

# Initial wealth
pgm.detNode(
    "initial",
    "Initial Wealth\nW0 = Buy-in",
    1.0, 3.3,
    scale=1.2,
    aspect=3.2
)

# Decision: stake fraction
pgm.decNode(
    "stake",
    "Stake Fraction f\n(decision)",
    4.0, 3.3,
    scale=1.2,
    aspect=3.2
)

# Random coin flip
pgm.latNode(
    "coin",
    "Coin Flip in Year t\nC ~ Bernoulli(0.5)",
    1.0, 1.5,
    scale=1.3,
    aspect=3.1
)


pgm.detNode(
    "wealth",
    "Wealth after Year t\nW(t) = prior wealth x factor",
    4.0, 1.5,
    scale=1.2,
    aspect=5.0
)

# Connect the nodes
pgm.add_edge("initial", "wealth")
pgm.add_edge("stake", "wealth")
pgm.add_edge("coin", "wealth")

# Repeat each year
pgm.add_plate(
    [0.0, 0.7, 5.2, 1.8],
    label="t = 1, ..., N"
)

# Save the image
output = Path("public/images/dag.png")
output.parent.mkdir(parents=True, exist_ok=True)

pgm.render()
pgm.savefig(str(output), dpi=300)

print("DAG saved to:", output)
