import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv("~/data_annotation/plot_data/geothermalinvestments.csv")

# Project Cost Visualization

# Determine which column to use for the x-axis label
x_axis_label = "Project Name" if df["Project Name"].nunique() > df["Project ID"].nunique() else "Project ID"

# Sort DataFrame by total cost in descending order
df_sorted_cost = df.sort_values(by="Total Project Cost (US$ milion)", ascending=False)

"""# Create a bar chart
plt.figure(figsize=(12, 6))
plt.bar(df_sorted_cost[x_axis_label], df_sorted_cost["Total Project Cost (US$ milion)"])
plt.xlabel(x_axis_label)
plt.ylabel("Total Project Cost (US$ milion)")
plt.title("Total Project Cost Breakdown")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()"""

# Contribution Visualization

# Filter out rows with missing "Region" values
df_filtered = df.dropna(subset=["Region"])

# Sort DataFrame by total contribution within each region (descending order)
df_sorted_region = (
    df_filtered.groupby(["Region", "Organization"])
    .agg(Total_Contribution=("Contribution by organization (US$ million)", "sum"))
    .unstack(fill_value=0)
)

# Flatten the multi-level index
df_sorted_region.columns = df_sorted_region.columns.get_level_values(1)

# Sort regions by total contribution (sum of contributions within each region)
df_sorted_region_sum = df_sorted_region.sum(axis=1).sort_values(ascending=False).index

# Reorder DataFrame based on sorted regions
df_sorted_region = df_sorted_region.loc[df_sorted_region_sum]

# Create a stacked bar chart

df_sorted_region.plot(kind="bar", stacked=True)
plt.xlabel("Region")
plt.ylabel("Contribution by Organization (US$ million)")
plt.title("Contribution by Organization per Region")
plt.legend(title="Organization")
plt.tight_layout()
plt.show()