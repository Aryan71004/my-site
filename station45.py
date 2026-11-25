
# Station 4.5: Pursuing Causation in the Wild
# Run-along 1: Explaining Away

import pandas as pd

print("\nRun-along 1: Explaining Away")

# Step 1: Define probabilities

p_difficulty = {"easy": 0.6, "hard": 0.4}

p_intelligence = {"low": 0.7, "high": 0.3}

p_grade = {
    ("low", "easy"): {"A": 0.30, "B": 0.40, "C": 0.30},
    ("low", "hard"): {"A": 0.05, "B": 0.25, "C": 0.70},
    ("high", "easy"): {"A": 0.90, "B": 0.08, "C": 0.02},
    ("high", "hard"): {"A": 0.50, "B": 0.30, "C": 0.20},
}

# Step 2: Build the table of probabilities

rows = []

for d, d_prob in p_difficulty.items():
    for i, i_prob in p_intelligence.items():
        for g, g_prob in p_grade[(i, d)].items():
            rows.append({
                "difficulty": d,
                "intelligence": i,
                "grade": g,
                "p": d_prob * i_prob * g_prob
            })

students = pd.DataFrame(rows)

print("\nFirst six rows:")
print(students.head(6))



# Step 3: Calculate conditional probabilities

def chance_high(table):
    high = table["intelligence"] == "high"
    return table.loc[high, "p"].sum() / table["p"].sum()

# Overall probability of high intelligence
print("\nOverall probability of high intelligence:")
print(round(chance_high(students), 3))

# Probability of high intelligence in a hard course
hard = students[students["difficulty"] == "hard"]

print("\nProbability of high intelligence in a hard course:")
print(round(chance_high(hard), 3))

# Probability of high intelligence given a B
got_b = students[students["grade"] == "B"]

print("\nProbability of high intelligence given a B:")
print(round(chance_high(got_b), 3))

# Probability of high intelligence given B in a hard course
got_b_hard = got_b[got_b["difficulty"] == "hard"]

print("\nProbability of high intelligence given B in a hard course:")
print(round(chance_high(got_b_hard), 3))



# Run-along 2: Berkeley Admissions
# Step 1: Load the admissions dataset

print("\nRun-along 2: Berkeley Admissions")

url = "https://raw.githubusercontent.com/rmcelreath/rethinking/master/data/UCBadmit.csv"
ucb = pd.read_csv(url, sep=";")


ucb = pd.read_csv(url, sep=";")

# Rename the gender column
ucb = ucb.rename(columns={"applicant.gender": "gender"})

print("\nFirst five rows:")
print(ucb.head())

# Calculate overall admission rates
overall = ucb.groupby("gender")[["admit", "applications"]].sum()

overall["rate"] = overall["admit"] / overall["applications"]

print("\nOverall admission rates:")
print(overall.round(3))



# Step 2: Compare admission rates by department

print("\nAdmission rates within each department:")

ucb["rate"] = (ucb["admit"] / ucb["applications"]).round(2)

print(
    ucb.pivot(
        index="dept",
        columns="gender",
        values="rate"
    )
)



# Step 3: Calculate where each gender applied

print("\nShare of applications by department and gender:")

total = ucb.groupby("gender")["applications"].transform("sum")

ucb["share"] = ucb["applications"] / total

print(
    ucb.pivot(
        index="dept",
        columns="gender",
        values="share"
    ).round(2)
)

