
# Station 4.3: Estimands, Estimators & The Fork
# Run-along 1: Simulate a Fork

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create a random number generator
rng = np.random.default_rng(42)

# Simulate 1,000 observations
n = 1000

# Z is the common cause
Z = rng.binomial(n=1, p=0.5, size=n)

# Both X and Y depend on Z
X = rng.binomial(n=1, p=0.1 + 0.8 * Z)
Y = rng.binomial(n=1, p=0.1 + 0.8 * Z)

# Store the results in a DataFrame
sim = pd.DataFrame({"Z": Z, "X": X, "Y": Y})

# Compare X and Y
print(pd.crosstab(sim["X"], sim["Y"]))

# Calculate the correlation
print("r =", round(sim["X"].corr(sim["Y"]), 2))



# Run-along 1, Part 2: Stratify by Z

print("\nStratifying by Z:")

for z in [0, 1]:
    inZ = sim[sim["Z"] == z]

    print(f"\nZ = {z}")
    print(pd.crosstab(inZ["X"], inZ["Y"]))
    print("r =", round(inZ["X"].corr(inZ["Y"]), 2))



# Run-along 1, Part 3: Continuous Fork Simulation

print("\nContinuous Fork Simulation:")

rng = np.random.default_rng(7)
n = 300

# Z is the common cause
Z = rng.binomial(n=1, p=0.5, size=n)

# X and Y are continuous variables that depend on Z
X = rng.normal(loc=2 * Z - 1, scale=1)
Y = rng.normal(loc=2 * Z - 1, scale=1)

# Create the scatter plot
fig, ax = plt.subplots(figsize=[6, 4.5], layout="constrained")

# Plot each Z group separately
for z, color in [(0, "#4E79A7"), (1, "#E15759")]:
    inZ = Z == z

    ax.scatter(
        X[inZ],
        Y[inZ],
        color=color,
        alpha=0.6,
        label=f"Z = {z}"
    )

    # Fit a regression line within each Z group
    slope, intercept = np.polyfit(X[inZ], Y[inZ], 1)

    print(f"slope within Z = {z}:", round(slope, 2))

    xs = np.linspace(X[inZ].min(), X[inZ].max(), 50)
    ax.plot(xs, intercept + slope * xs, color=color, linewidth=2.5)

# Fit a regression line using all observations
slope, intercept = np.polyfit(X, Y, 1)

print("slope, all data:", round(slope, 2))

xs = np.linspace(X.min(), X.max(), 50)

ax.plot(
    xs,
    intercept + slope * xs,
    color="black",
    linewidth=2.5,
    label="all data"
)

# Add labels and title
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("Within Each Value of Z, X Tells You Nothing About Y")
ax.legend()

plt.show()



# Run-along 2: Doc Dreamy and Doc Duck
# Step 1: Load patient data

print("\nRun-along 2: Doc Dreamy and Doc Duck")

url = "https://flyaflya.github.io/confounderChallenge/"
patients = pd.read_csv(url + "patients_data.csv")

print(patients.shape)
print(patients.head(3))



# Step 2: Compare average symptom scores

print("\nAverage post-surgical scores by surgeon:")

print(
    patients.groupby("doctor_name")["post_surgical_score"]
    .agg(["count", "mean"])
    .round(2)
)



# Step 3: Compare patient severity by surgeon

print("\nAverage patient severity by surgeon:")

print(
    patients.groupby("doctor_name")["severity"]
    .mean()
    .round(2)
)



# Run-along 2: Compare patients with similar severity
# Step 4: Stratify by severity

print("\nComparing patients with similar severity:")

similar = patients[patients["severity"].between(-1, 1)]

print(
    similar.groupby("doctor_name")["post_surgical_score"]
    .agg(["count", "mean"])
    .round(2)
)



# Step 5: Visualize outcomes by patient severity

fig, ax = plt.subplots(figsize=[7, 4.3], layout="constrained")

# Shade the comparable severity range
ax.axvspan(-1, 1, color="khaki", alpha=0.35)

# Plot each surgeon's patients
for name, color, marker in [
    ("Doc Dreamy", "#4E79A7", "o"),
    ("Doc Duck", "#E15759", "^")
]:

    docDF = patients[patients["doctor_name"] == name]

    ax.scatter(
        docDF["severity"],
        docDF["post_surgical_score"],
        color=color,
        marker=marker,
        alpha=0.75,
        label=name
    )

    # Average outcome within the similar-severity range
    bandMean = similar.loc[
        similar["doctor_name"] == name,
        "post_surgical_score"
    ].mean()

    # Draw the average line across the shaded area
    ax.hlines(
        bandMean,
        -1,
        1,
        color=color,
        linestyle="--",
        linewidth=2
    )

# Add chart labels
ax.set_xlabel("Initial Patient Severity")
ax.set_ylabel("Post-Surgical Symptom Score (lower is better)")

ax.set_title(
    "Among Similar Patients, Doc Duck Scores 0.29 Lower (Better)"
)

ax.legend(loc="upper left")

plt.show()



# Run-along 2: Randomized Experiment
# Compare Doc Dreamy and Doc Duck with random assignment

print("\nRandomized experiment results:")

randomized = pd.read_csv(url + "patients_data_randomized.csv")

print("\nAverage post-surgical scores:")
print(
    randomized.groupby("doctor_name")["post_surgical_score"]
    .agg(["count", "mean"])
    .round(2)
)

print("\nAverage patient severity:")
print(
    randomized.groupby("doctor_name")["severity"]
    .mean()
    .round(2)
)



# Step 4: Visualize the randomized experiment

fig, ax = plt.subplots(figsize=[7, 4.3], layout="constrained")

for name, color, marker in [
    ("Doc Dreamy", "#4E79A7", "o"),
    ("Doc Duck", "#E15759", "^")
]:
    docDF = randomized[randomized["doctor_name"] == name]

    ax.scatter(
        docDF["patient"],
        docDF["post_surgical_score"],
        color=color,
        marker=marker,
        alpha=0.75,
        label=name
    )

    average = docDF["post_surgical_score"].mean()

    ax.axhline(
        average,
        color=color,
        linestyle="--",
        linewidth=2
    )

    ax.text(
        randomized["patient"].max(),
        average,
        f"mean={average:.2f}",
        color=color,
        va="bottom",
        ha="right"
    )

ax.set_xlabel("Patient (assigned to a surgeon at random)")
ax.set_ylabel("Post-Surgical Symptom Score (lower is better)")
ax.set_title("With Random Assignment, Doc Duck Scores 0.75 Lower (Better)")
ax.legend(loc="upper left")

plt.show()

