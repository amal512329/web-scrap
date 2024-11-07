import pandas as pd

# Function to create a CSV file with specified columns
def create_csv_file(csv_file_name, columns=['urls', 'data']):
    """
    Creates a CSV file with the given column names.

    Args:
    - csv_file_name (str): The name of the CSV file to create.
    - columns (list): A list of column names to include in the CSV file.
    """
    # Create a DataFrame with the specified columns
    df = pd.DataFrame(columns=columns)
    
    # Save the DataFrame to a CSV file with the specified file name
    df.to_csv(csv_file_name, index=False)  # 'index=False' to avoid writing row numbers
    
    print(f"CSV file '{csv_file_name}' created with columns: {', '.join(columns)}")

# Example usage
create_csv_file('output_data.csv', ['urls', 'site'])  # Create CSV with 'urls' and 'site' columns
