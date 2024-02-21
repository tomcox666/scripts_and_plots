import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("../plot_data/ZGNX_testscores.csv")

# Group the data by gender
gender_groups = df.groupby("gender")

# Calculate descriptive statistics for each gender group
gender_stats = gender_groups[["algebra", "english", "science"]].describe()

# Print the descriptive statistics
print(gender_stats)

# Create box plots for each subject
subjects = ["algebra", "english", "science"]

fig, axes = plt.subplots(nrows=1, ncols=len(subjects), figsize=(15, 5))

for i, subject in enumerate(subjects):
    df.boxplot(by="gender", column=subject, ax=axes[i], vert=False)
    axes[i].set_xlabel(subject)
    axes[i].set_title(f"{subject} Scores by Gender")

plt.tight_layout()
plt.show()