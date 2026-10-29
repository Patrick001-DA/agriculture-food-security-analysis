"""Agriculture & food security analysis with pandas.

Explores rainfall, crop production, yield and a simple food-security index
across four Kenyan counties (Kajiado, Machakos, Nakuru, Nyeri), January-June.
All figures in the dataset are fictional.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path("data/06_agriculture_food_security.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

# ---- Inspect the dataset ----
print("Rows:", len(df))
df.info()
print("Shape:", df.shape)
print(df.describe().to_string())
print("Columns:", list(df.columns))

# ---- Clean the dataset ----
print("\nMissing values:\n", df.isna().sum())
print("Duplicate rows:", df.duplicated().sum())

# ---- Average rainfall and crop production per county ----
average_by_county = (
    df.groupby("county")[["crop_production_tonnes", "rainfall_mm"]].mean().round(2)
)
print("\nAverage by county:\n", average_by_county)

# ---- County with the highest total crop production ----
total_production = (
    df.groupby("county")["crop_production_tonnes"].sum().sort_values(ascending=False)
)
print("\nTotal production by county:\n", total_production)

# ---- Month with the highest average rainfall across counties ----
avg_rainfall_by_month = (
    df.groupby("month")["rainfall_mm"].mean().sort_values(ascending=False).round(2)
)
print("\nAverage rainfall by month:\n", avg_rainfall_by_month)

# ---- Percentage change in production, January to June ----
wide = df.pivot(index="county", columns="month", values="crop_production_tonnes")
wide["pct_change_jan_to_jun"] = (wide["Jun"] - wide["Jan"]) / wide["Jan"] * 100
print("\nPercentage change in production (Jan to Jun):\n",
      wide[["pct_change_jan_to_jun"]].round(2))

# ---- Correlation between rainfall and crop production ----
correlation = df["rainfall_mm"].corr(df["crop_production_tonnes"])
print("\nRainfall vs crop production correlation:", round(correlation, 2))

# ---- Line chart: monthly crop production by county ----
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
fig, ax = plt.subplots()
for county, group in df.groupby("county"):
    group = group.set_index("month").loc[month_order]
    ax.plot(group.index, group["crop_production_tonnes"], marker="o", label=county)
ax.set_title("Monthly Crop Production by County")
ax.set_xlabel("Month")
ax.set_ylabel("Production (tonnes)")
ax.legend()
fig.tight_layout()

# Save BEFORE show(): show() can clear the figure and give a blank file
fig.savefig(OUTPUT_DIR / "agriculture_food_security.png", dpi=150)
fig.savefig(OUTPUT_DIR / "agriculture_food_security.pdf")
plt.show()
