
# Station 4.4: The Elemental Confounds
# Run-along 1: The Pipe

import numpy as np
import pandas as pd

# Create the random number generator
rng = np.random.default_rng(11)

# Simulate 100 plants
n = 100

# Randomly assign pesticide
pesticide = rng.binomial(n=1, p=0.5, size=n)

# Pesticide reduces the probability of fungus
fungus = rng.binomial(n=1, p=0.8 - 0.6 * pesticide)

# Fungus reduces plant growth
growth = 10 - 4 * fungus + rng.normal(loc=0, scale=1.5, size=n)

# Store results in a DataFrame
plants = pd.DataFrame({
    "pesticide": pesticide,
    "fungus": fungus,
    "growth": growth
})

print("\nFirst five plants:")
print(plants.head().round(2))



# Step 2: Compare overall plant growth

print("\nAverage growth by pesticide treatment:")
print(plants.groupby("pesticide")["growth"].mean().round(2))

print("\nPesticide and fungus counts:")
print(pd.crosstab(plants["pesticide"], plants["fungus"]))



# Step 3: Stratify by fungus

print("\nAverage growth within each fungus group:")

print(
    plants.groupby(["fungus", "pesticide"])["growth"]
    .agg(["count", "mean"])
    .round(2)
)



# Run-along 2: The Collider
# Step 1: Simulate 1,000 surgeons

print("\nRun-along 2: The Collider")

rng = np.random.default_rng(2026)
n = 1000

# Generate independent competence and charisma scores
competence = rng.normal(loc=0, scale=1, size=n)
charisma = rng.normal(loc=0, scale=1, size=n)

# Create the surgeons DataFrame
surgeons = pd.DataFrame({
    "competence": competence,
    "charisma": charisma
})

# Prestigious jobs depend on competence + charisma
surgeons["score"] = surgeons["competence"] + surgeons["charisma"]

# Only the top 10% receive prestigious jobs
cutoff = surgeons["score"].quantile(0.9)

surgeons["prestigious"] = surgeons["score"] > cutoff

# Display the first five surgeons
print(surgeons.head().round(2))

print("cutoff:", round(cutoff, 2))



# Step 2: Compare correlations

print("\nCorrelations between competence and charisma:")

# Correlation across all 1,000 surgeons
r_all = surgeons["competence"].corr(surgeons["charisma"])

# Surgeons with prestigious jobs
top = surgeons[surgeons["prestigious"]]
r_top = top["competence"].corr(top["charisma"])

print("all surgeons:", round(r_all, 2))
print("prestigious jobs:", len(top), round(r_top, 2))

# Surgeons without prestigious jobs
rest = surgeons[~surgeons["prestigious"]]
r_rest = rest["competence"].corr(rest["charisma"])

print("everyone else:", len(rest), round(r_rest, 2))



# Step 3: Visualize the collider

import matplotlib.pyplot as plt

fig, axs = plt.subplots(
    ncols=2,
    figsize=(10, 4.5),
    layout="constrained",
    sharex=True,
    sharey=True
)

# Left chart: all 1,000 surgeons
axs[0].scatter(
    rest["competence"],
    rest["charisma"],
    color="lightgrey",
    alpha=0.7
)

axs[0].scatter(
    top["competence"],
    top["charisma"],
    color="goldenrod",
    alpha=0.85,
    label="Prestigious job (top 10%)"
)

axs[0].set_title(f"All 1,000 Surgeons: r = {r_all:.2f}")
axs[0].set_xlabel("Competence")
axs[0].set_ylabel("Charisma")
axs[0].legend(loc="lower left")

# Right chart: prestigious surgeons only
axs[1].scatter(
    top["competence"],
    top["charisma"],
    color="goldenrod",
    alpha=0.85
)

# Add regression line
slope, intercept = np.polyfit(
    top["competence"],
    top["charisma"],
    1
)

xs = np.linspace(
    top["competence"].min(),
    top["competence"].max(),
    50
)

axs[1].plot(
    xs,
    intercept + slope * xs,
    color="black",
    linewidth=2
)

axs[1].set_title(
    f"Only the 100 in Prestigious Jobs: r = {r_top:.2f}"
)

axs[1].set_xlabel("Competence")

plt.show()
