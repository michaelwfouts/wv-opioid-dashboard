import pandas as pd

def clean_csv_columns(csv_path):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_path)

        # Specific Cleaning of Datasets
        if csv_path == 'data\WV Drug Epidemic Dataset.xlsx - Illicit Drug Past Mo (Percent).csv':
            # Removing regions to loop year correlations
            columns_to_remove = [col for col in df.columns if 'Region' in col]
            df = df.drop(columns=columns_to_remove)
            # Expanded columns manually
            
        if csv_path == 'data\WV Drug Epidemic Dataset.xlsx - Illicit Drug Past Mo (Percent).csv':
            columns_to_remove = [col for col in df.columns if 'Region' in col]
            df = df.drop(columns=columns_to_remove)

        # Iterate through each column (excluding the first column) and clean the values
        for col in df.columns[1:]:
            if df[col].dtype == 'O':  # Check if the column has object (string) dtype
                # Remove commas from string values and convert to numeric
                df[col] = df[col].replace(',', '', regex=True)
                df[col] = df[col].replace('%', '', regex=True)
                df[col] = pd.to_numeric(df[col])

        # Drop rows where all values are NaN
        df = df.dropna(how='all')

        # Write the cleaned DataFrame back to the CSV file
        df.to_csv(csv_path, index=False)

        print(f"Columns in '{csv_path}' have been cleaned successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# Replace 'your_file_path.csv' with the actual path to your CSV file
clean_csv_columns('data\WV Drug Epidemic Dataset.xlsx - Illicit Drug Past Mo (Percent).csv')