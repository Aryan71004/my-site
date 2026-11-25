
import pandas as pd

url = "https://raw.githubusercontent.com/flyaflya/persuasive/main/starwars.csv"
sw = pd.read_csv(url, usecols=["name", "height", "mass", "homeworld", "species"])
print(sw.shape)
print(sw.head())


# Move 1: Assign - convert height to inches
print("\nHeight in inches:")
print(sw.assign(inches=lambda df: df["height"] / 2.54).head())


# Move 1: Chain two assignments - calculate BMI
print("\nHeight in meters and BMI:")
print(
    sw
    .assign(height_m=lambda df: df["height"] / 100)
    .assign(bmi=lambda df: df["mass"] / df["height_m"] ** 2)
    .head()
)


# Move 2: Subset - select rows
print("\nWookiee characters:")
print(sw.query('species == "Wookiee"'))


# Move 2: Subset - select columns
print("\nNames and species:")
print(sw.filter(["name", "species"]).head())


# Move 2: Combine row and column selection
print("\nDroids and Wookiees:")
print(
    sw
    .query('species in ["Droid", "Wookiee"]')
    .filter(["name", "species", "height"])
)


# Move 3: Drop - remove rows with missing height or mass
print("\nRemove missing values:")
clean = sw.dropna(subset=["height", "mass"])
print(len(sw), len(clean))


# Move 3: Drop - remove the homeworld column
print("\nWithout the homeworld column:")
print(clean.drop(columns=["homeworld"]).head())


# Move 4: Sort - tallest characters first
print("\nTallest Star Wars characters:")
print(sw.sort_values("height", ascending=False).head())


# Move 4: Sort and reset row numbers
print("\nTallest characters with a new index:")
print(
    sw
    .sort_values("height", ascending=False)
    .reset_index(drop=True)
    .head()
)


# Move 5: Aggregate - calculate average height
print("\nAverage character height:")
print(sw.agg({"height": ["mean"]}))


# Move 5: Aggregate - calculate multiple statistics
print("\nHeight and mass summary:")
print(sw.agg({"height": ["mean", "max"], "mass": ["mean"]}).round(1))



# Move 6: Merge - create a second DataFrame
print("\nPlanet climate information:")

worlds = pd.DataFrame({
    "homeworld": ["Tatooine", "Kashyyyk", "Naboo"],
    "climate": ["arid", "tropical", "temperate"],
})

print(worlds)



# Move 6: Merge using a left join
print("\nMerged Star Wars data:")

joined = sw.merge(worlds, on="homeworld", how="left")
print(joined.head())



# Move 6: Compare left and inner joins
print("\nLeft join row counts:")
print(len(sw), len(joined))

print("\nInner join row count:")
print(len(sw.merge(worlds, on="homeworld", how="inner")))


# Move 7: Split-Apply-Combine
print("\nAverage height by species:")

print(
    sw.groupby("species")
    .agg(avgHeight=("height", "mean"), count=("name", "count"))
    .sort_values("count", ascending=False)
    .round(0)
    .head()
)


# Run-along 2: Answering the CEO
# Step 1: Load shipment data

print("\nStep 1: Shipment data types")

ship_url = "https://raw.githubusercontent.com/flyaflya/persuasive/main/shipments.csv"

shipments = pd.read_csv(
    ship_url, parse_dates=["plannedShipDate", "actualShipDate"]
).head(4000)

print(shipments.dtypes)


# Step 2: Identify late shipments

print("\nStep 2: Late shipment indicator")

late = shipments.assign(
    is_late=lambda df: df["actualShipDate"] > df["plannedShipDate"]
)

print(late.head(3))


# Step 3: Count late shipments

print("\nStep 3: Number of late shipment lines")
print(late["is_late"].sum())

print("\nStep 3: Proportion of late shipment lines")
print(late["is_late"].mean())


# Step 4: Merge product categories
print("\nStep 4: Merge product categories")

prod_url = "https://raw.githubusercontent.com/flyaflya/persuasive/main/productLine.csv"
products = pd.read_csv(prod_url)

merged = late.merge(products, on="partID", how="left")

print(len(late), len(merged))
print(merged["prodCategory"].isna().sum())




# Debugging a Chain: Dates read as text
print("\nDebugging: Dates loaded as text")

raw = pd.read_csv(ship_url).head(4000)

bad = raw.assign(
    is_late=lambda df: df["actualShipDate"] > df["plannedShipDate"]
)

print(raw["plannedShipDate"].dtype)
print(bad["is_late"].sum())





# Debugging a Chain: Use np.where instead of if
import numpy as np

print("\nCorrect shipment status labels:")

labeled = late.assign(
    status=lambda df: np.where(df["is_late"], "Late", "On time")
)

print(labeled[["shipID", "is_late", "status"]].head())
