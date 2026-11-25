
# Station 4.2: Data Visualization
# Stage 2: Curation of Content
# Run-along 1: Decision alternatives

import matplotlib.pyplot as plt

# Five decision alternatives and their satisfaction scores
decisionArray = ["A", "B", "C", "D", "E"]
satisfactionArray = [3, 5, 4, 3, 1]

# Find the highest utility score
bestUtility = max(satisfactionArray)

# Highlight the best alternative in purple
colorArray = [
    "darkorchid" if utilityVal == bestUtility else "lightgrey"
    for utilityVal in satisfactionArray
]

print(colorArray)

# Create the bar chart
fig, ax = plt.subplots(figsize=[5, 3.5], layout="constrained")

ax.bar(
    x=decisionArray,
    height=satisfactionArray,
    color=colorArray
)

# Add labels and title
ax.set_xlabel("Decision Alternative")
ax.set_ylabel("Utility")
ax.set_title("Decision B is the Best Alternative")

# Display the chart
plt.show()



# Stage 3: Facets - Compare decisions by region
import pandas as pd

regionArray = ["East", "East", "West", "West", "West"]

plotDF = pd.DataFrame({
    "decision": decisionArray,
    "satisfaction": satisfactionArray,
    "region": regionArray
})

# Create two charts side by side
fig, axs = plt.subplots(
    ncols=2,
    figsize=[8, 3.5],
    layout="constrained",
    sharey=True
)

for idx, (region, groupDF) in enumerate(plotDF.groupby("region")):
    best = groupDF["satisfaction"].max()

    colors = [
        "darkorchid" if u == best else "lightgrey"
        for u in groupDF["satisfaction"]
    ]

    bestLabel = groupDF.loc[
        groupDF["satisfaction"].idxmax(), "decision"
    ]

    axs[idx].bar(
        x=groupDF["decision"],
        height=groupDF["satisfaction"],
        color=colors
    )

    axs[idx].set_xlabel("Decision Alternative")
    axs[idx].set_ylabel("Utility")
    axs[idx].set_title(f"{region}: Decision {bestLabel} is Best")

fig.suptitle("The Best Decision Differs by Region")

plt.show()



# Stage 4: Formatting for your audience
# Run-along 2, Part 1: Add a legend and annotation

fig, ax = plt.subplots(figsize=[5, 3.5], layout="constrained")

ax.set_title("Decision B is the Best Alternative")
ax.set_xlabel("Decision Alternative")
ax.set_ylabel("Utility")

# Draw bars individually so the legend can identify the colors
for decision, satisfaction in zip(decisionArray, satisfactionArray):
    if satisfaction == bestUtility:
        reco = ax.bar(
            decision,
            satisfaction,
            color="darkorchid",
            label="Recommended"
        )
    else:
        unwise = ax.bar(
            decision,
            satisfaction,
            color="lightgrey",
            label="Not recommended"
        )

# Add the legend
ax.legend(handles=[reco, unwise])

# Add the annotation with an arrow
ax.annotate(
    text="Consider Decision C if sustainability\nmatters. Utility does not include it.",
    xy=("C", 4.05),
    xytext=("D", 2.2),
    horizontalalignment="center",
    arrowprops={"arrowstyle": "->"}
)

plt.show()



# Run-along 2, Part 2: The Coors chart
# Step 1: Load baseball data

import pandas as pd

print("\nBaseball data:")

url = "https://raw.githubusercontent.com/flyaflya/persuasive/main/baseball10.csv"
games = pd.read_csv(url)

print(games.shape)
print(games.head(3))



# Step 2: Calculate average runs by ballpark

print("\nAverage runs by ballpark:")

avgDF = (
    games
    .assign(totalRuns=lambda df: df["homeScore"] + df["visScore"])
    .drop(columns=["date", "visiting"])
    .groupby("home")
    .mean()
    .sort_values("totalRuns")
    .reset_index()
)

print(avgDF.tail(3).round(2))




# Run-along 2, Part 2: Final Coors Field chart

print("\nCreating the Colorado ballpark chart...")

league = avgDF["totalRuns"].mean()

colorArray = [
    "darkorchid" if team == "COL" else "lightgrey"
    for team in avgDF["home"]
]

fig, ax = plt.subplots(figsize=[6.5, 7], layout="constrained")

ax.barh(avgDF["home"], avgDF["totalRuns"], color=colorArray)

ax.axvline(league, color="black", linestyle="--", linewidth=1)

ax.set_title("Colorado (COL) Is the Most Run-Friendly Ballpark in 2010")
ax.set_xlabel("Average Runs per Game (both teams)")
ax.set_ylabel("Ballpark (home team)")

ax.annotate(
    text="COL: 10.59 runs a game,\n21% above the league\naverage of 8.77 (dashed line)",
    xy=(10.59, "COL"),
    xytext=(2.0, "CHA"),
    arrowprops={"arrowstyle": "->"}
)

plt.show()



# Run-along 2: Compare 2010 and 2021
# Facet the baseball chart by year

print("\nComparing ballparks in 2010 and 2021...")

fig, axs = plt.subplots(
    ncols=2,
    figsize=[10, 7],
    layout="constrained",
    sharex=True
)

for idx, year in enumerate(["10", "21"]):

    yearDF = (
        pd.read_csv(
            f"https://raw.githubusercontent.com/flyaflya/persuasive/main/baseball{year}.csv"
        )
        .assign(
            totalRuns=lambda df: df["homeScore"] + df["visScore"]
        )
        .drop(columns=["date", "visiting"])
        .groupby("home")
        .mean()
        .sort_values("totalRuns")
        .reset_index()
    )

    colors = [
        "darkorchid" if team == "COL" else "lightgrey"
        for team in yearDF["home"]
    ]

    axs[idx].barh(
        yearDF["home"],
        yearDF["totalRuns"],
        color=colors
    )

    axs[idx].set_title(f"20{year}")
    axs[idx].set_xlabel("Average Runs per Game (both teams)")

axs[0].set_ylabel("Ballpark (home team)")

fig.suptitle(
    "Coors Field (COL) Led Baseball in Runs in 2010 but Ranked Third in 2021"
)

plt.show()
