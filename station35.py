
import numpy as np
rng = np.random.default_rng(seed=21)
n = 100_000

# 100,000 simulated Tuesdays under EACH alternative
total_a = rng.poisson(18, n) + rng.poisson(37, n)  # Patrick at Shop 1
total_b = rng.poisson(11, n) + rng.poisson(49, n)  # Patrick at Shop 4

print(total_a.mean(), total_b.mean())

diff = total_b - total_a
print(diff.mean())
print((diff > 0).mean())
print(np.quantile(diff, [0.05, 0.95]))


# Run-along 2: Sensitivity analysis

total_b_low = rng.poisson(11, n) + rng.poisson(45, n)

print((total_b_low - total_a).mean())
print((total_b_low > total_a).mean())



# Run-along 3: Draw Patrick's decision DAG

from functools import partialmethod
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

pgm.decNode(
    "where",
    "WherePatrick\n(decision: Shop 1 or Shop 4)",
    1, 2.2,
    scale=1.6,
    aspect=4.0
)

pgm.latNode(
    "s1",
    "CarsFixed at Shop 1\n" + r"$\sim Poisson(\lambda_1)$",
    1.0, 1,
    scale=1.5,
    aspect=3.6
)

pgm.latNode(
    "s4",
    "CarsFixed at Shop 4\n" + r"$\sim Poisson(\lambda_4)$",
    3.0, 1,
    scale=1.5,
    aspect=3.6
)

pgm.add_edge("where", "s1")
pgm.add_edge("where", "s4")

pgm.render()
pgm.savefig("patrick_dag.png", dpi=300)
