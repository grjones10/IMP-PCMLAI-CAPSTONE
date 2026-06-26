from pathlib import Path
import numpy as np
import pandas as pd

from pathlib import Path

def get_X_cols(df):
    return [col for col in df.columns if col.startswith("X")]

def get_working_week(week, function):

    DIR = Path.cwd().parent

    data_folder_name = f"function_{function}"
    week_folder_name = f"week_{week}"

    return DIR, data_folder_name, week_folder_name

def create_results_dir(week_folder_name, data_folder_name):

    DIR = Path.cwd().parent

    p = Path(DIR / "results" / "plots" / week_folder_name / data_folder_name)
    p.mkdir(parents=True, exist_ok=True)

    return p

def load_initial_data(PROJECT_DIR, folder_name):

    folder_path = PROJECT_DIR / "data" / "initial_data" / folder_name

    input_file = folder_path / "initial_inputs.npy"
    output_file = folder_path / "initial_outputs.npy"

    for f in [input_file, output_file]:
        if not f.exists():
            raise FileNotFoundError(f"\tFile not found: {f}")

    input_data = np.load(input_file)
    output_data = np.load(output_file)

    df_input = pd.DataFrame(
        input_data,
        columns=[f"X{i+1}" for i in range(input_data.shape[1])]
    )

    if output_data.ndim == 1:
        output_data = output_data.reshape(-1, 1)

    df_output = pd.DataFrame(
        output_data,
        columns=[f"Y{i+1}" for i in range(output_data.shape[1])]
    )

    df = pd.concat([df_input, df_output], axis=1)

    print(f"\tLoaded initial data: {folder_name}")

    return df

import os
import csv

def append_results(results_dir, test_name, result_dict):
    """
    Appends experiment results to a CSV file with numeric values
    formatted to 6 decimal places.
    """

    results_dir = results_dir.parent
    
    os.makedirs(results_dir, exist_ok=True)
    file_path = os.path.join(results_dir, "results.csv")

    fieldnames = ["test_name"] + list(result_dict.keys())
    file_exists = os.path.isfile(file_path)

    def format_value(v):
        if isinstance(v, (int, float)):
            return f"{v:.6f}"
        return v

    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        row = {"test_name": test_name}
        row.update({k: format_value(v) for k, v in result_dict.items()})

        writer.writerow(row)

def apply_updates(df, week, folder_name):

    """
    Applies updates from CSV files in 'data/updated_data' for the specified folder_name.
    Adds a "new data point" column: 0 = initial data, 1 = new data.
    Matching is case-insensitive.
    Returns a single updated DataFrame with all columns.
    """

    import ast
    import re

    DIR = Path.cwd().parent
    UPDATED_DATA_DIR = DIR / "data/updated_data"

    # ----------------------------
    # Ensure flag column exists
    # ----------------------------
    df = df.copy()
    df["new data point"] = 0

    # ----------------------------
    # Find update files
    # ----------------------------
    csv_files = list(UPDATED_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("\nNo update files found.")
        return df

    print("\tAvailable update files:")
    for i, file in enumerate(csv_files, start=1):
        print(f"\t\t{i}: {file.name}")

    # ----------------------------
    # Parse selection
    # ----------------------------

    selected_files = []

    for f in csv_files:
        name = os.path.basename(f).lower()
        match = re.search(r"wk(\d+)", name)  # extract number after 'wk'
        
        if match:
            file_week = int(match.group(1))
            if 1 <= file_week < week:
                selected_files.append(f)

    if not selected_files:
        print(f"\tNo files found for weeks 1 to {week-1}.")
        return df

    # ----------------------------
    # Prepare new rows
    # ----------------------------
    new_rows = []

    folder_name_lower = folder_name.lower()

    for file in selected_files:
        df_updates = pd.read_csv(file)

        # Case-insensitive matching
        func_names_lower = df_updates["function name"].str.lower()
        mask = func_names_lower == folder_name_lower
        df_func = df_updates[mask]

        if df_func.empty:
            print(f"\tNo matching rows in {file.name}")
            continue

        for _, row in df_func.iterrows():
            try:
                # Convert inputs string to list
                # print(row)
                inputs = ast.literal_eval(row["inputs"])
                output = float(row["outputs"])
                
                # Each input dimension becomes its own column (X1, X2, ...)
                row_data = inputs + [output, 1]  # last 1 = "new data point" flag
                new_rows.append(row_data)

            except Exception as e:
                print(f"\tFailed to parse row in {file.name}: {e}")

    if not new_rows:
        print("\tNo valid updates found.")
        return df

    # ----------------------------
    # Create DataFrame for new rows
    # ----------------------------
    columns = list(df.columns)
    df_new = pd.DataFrame(new_rows, columns=columns)

    # ----------------------------
    # Combine + deduplicate
    # ----------------------------
    df = pd.concat([df, df_new], ignore_index=True)

    # Keep the newest version if duplicates exist (prefer flag=1)
    subset_cols = [c for c in df.columns if c != "new data point"]
    df = df.sort_values("new data point").drop_duplicates(subset=subset_cols, keep="last")
    df = df.reset_index(drop=True)

    print(f"\tAdded {len(df_new)} new data points.")

    return df
 