def preprocess_all_turn_snapshots(input_folder: Path, output_csv: Path | None = None) -> pd.DataFrame:
    """
    Read all turn_snapshots_*.csv under folder, preprocess each into 1 row,
    and combine into a single dataframe.
    """
    files = sorted(input_folder.glob("turn_snapshots_*.csv"))

    if not files:
        raise FileNotFoundError(f"No turn_snapshots_*.csv files found in: {input_folder}")

    all_rows = []

    for file_path in files:
        print(f"Processing: {file_path.name}")
        row = preprocess_turn_snapshot_file(file_path)
        if row is not None:
            all_rows.append(row)

    if not all_rows:
        raise ValueError("No valid turn snapshot files were successfully processed.")

    all_features_df = pd.DataFrame(all_rows)

    # optional: sort by session_id
    if "session_id" in all_features_df.columns:
        all_features_df = all_features_df.sort_values("session_id").reset_index(drop=True)

    if output_csv is not None:
        all_features_df.to_csv(output_csv, index=False)
        print(f"\nSaved combined features to: {output_csv}")

    return all_features_df