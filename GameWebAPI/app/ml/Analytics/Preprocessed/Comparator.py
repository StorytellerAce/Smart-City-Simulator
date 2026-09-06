import pandas as pd
import numpy as np

folder = r"C:\UnityProjects\FYP\GameWebAPI\app\ml\Analytics\Preprocessed"

old = pd.read_csv(f"{folder}\\session_features.csv")
new = pd.read_csv(f"{folder}\\session_features2.csv")

merged = old.merge(
    new,
    on="session_id",
    suffixes=("_old", "_new"),
    how="outer"
)

feature_columns = [
    col for col in old.columns
    if col != "session_id"
]

summary = []

for col in feature_columns:

    old_col = f"{col}_old"
    new_col = f"{col}_new"

    changed = ~np.isclose(
        merged[old_col],
        merged[new_col],
        equal_nan=True
    )

    summary.append({
        "feature": col,
        "sessions_changed": changed.sum(),
        "max_difference": (
            (merged[old_col] - merged[new_col])
            .abs()
            .max()
        ),
        "mean_difference": (
            (merged[old_col] - merged[new_col])
            .abs()
            .mean()
        )
    })

summary_df = pd.DataFrame(summary)

print(summary_df.to_string(index=False))