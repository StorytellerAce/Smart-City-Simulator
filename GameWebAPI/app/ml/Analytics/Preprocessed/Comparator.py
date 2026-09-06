import pandas as pd

folder = r"C:\UnityProjects\FYP\GameWebAPI\app\ml\Analytics\Preprocessed"

old = pd.read_csv(folder + r"\session_features.csv")
new = pd.read_csv(folder + r"\session_features2.csv")

# Check shape
print("Old shape:", old.shape)
print("New shape:", new.shape)

# Check columns
print("\nColumns only in old:")
print(set(old.columns) - set(new.columns))

print("\nColumns only in new:")
print(set(new.columns) - set(old.columns))

# Compare common columns/rows
common_columns = list(set(old.columns) & set(new.columns))

old_common = old[common_columns]
new_common = new[common_columns]

# Sort so row ordering doesn't matter
old_common = old_common.sort_values(common_columns).reset_index(drop=True)
new_common = new_common.sort_values(common_columns).reset_index(drop=True)

print("\nSame contents:", old_common.equals(new_common))