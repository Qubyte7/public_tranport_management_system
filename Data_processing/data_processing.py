import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# gloabal variables
CLIENT_CACHE_FILE_DATAFRAMES = "./data_screenshot/clients_cached_dataframes.csv"
BOOKEDTICKETS_CACHE_FILE_DATAFRAMES =  "./data_screenshot/bookedtickets_cached_dataframes.csv"
CACHE_FILE_VALIDITY_DAYS = 1

def is_cache_valid(file_path):
    # checking if the file is valid
    if not os.path.exists(file_path):
        return False
    file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    return  datetime.now() - file_mod_time < timedelta(days=CACHE_FILE_VALIDITY_DAYS)

def fetch_all_records(api_url,page_size=1000):
    page=1
    all_records = []
    while True:
        response = requests.get(api_url,params={'page':page,'page_size':page_size})
        response.raise_for_status()
        data = response.json()
        #print(data)
        # extract client data and total amount
        records_from_current_page = data["data"]
        # adding clients into a list
        all_records.extend(records_from_current_page)
        if len(records_from_current_page) < page_size:
            break
        # move to the next page
        page+=1
    return all_records

def get_or_create_dataframe_excel_file(api_url,CACHE_DATAFRAME_FILE):
    """Get data, using cache if valid."""
    if is_cache_valid(CACHE_DATAFRAME_FILE):
        print("Using cached data.")
        # Load data from the cache
        return pd.read_csv(CACHE_DATAFRAME_FILE)
    print("Fetching fresh data from API.")
    # Fetch fresh data
    clients = fetch_all_records(api_url)
    # Convert to DataFrame
    df = pd.DataFrame(clients)
    # Save to Excel cache
    df.to_csv(CACHE_DATAFRAME_FILE, index=False) # index is set to false because we are omitting to save index to our excel also
    return df

try:
    clients_dataframes = get_or_create_dataframe_excel_file('http://127.0.0.1:8000/app/v1/clients',CLIENT_CACHE_FILE_DATAFRAMES)
    booked_tickets_dataframes = get_or_create_dataframe_excel_file('http://127.0.0.1:8000/app/v1/booked_tickets',BOOKEDTICKETS_CACHE_FILE_DATAFRAMES)
    print("check ON the data_screenshot directory.")
    # Fetch data from API
    # with pagination
    # clients_api_data = fetch_all_clients('http://127.0.0.1:8000/app/v1/clients')
    # booked_tickets_api_data = fetch_all_clients('http://127.0.0.1:8000/app/v1/booked')

    # Load data into DataFrames
    # clients_data_frames = pd.DataFrame(clients_api_data)
    # booked_tickets_data_frames = pd.DataFrame(booked_tickets_api_data)

    # Check DataFrames (if they are large, this can be omitted)
    # print(clients_data_frames.describe())
    # print(booked_tickets_data_frames.describe())
    # print(clients_data_frames.columns)
    # print(booked_tickets_data_frames.columns)

    # Merging datasets based on 'id' (adjust 'id' if needed)
    # inner_merged_df = pd.merge(clients_data_frames, booked_tickets_data_frames, left_on='id', right_on='client_id',how='inner')
    # print(inner_merged_df.shape)  # Print the shape of the merged dataset

    # Check for missing values
    # print(inner_merged_df.isnull().sum())

    # Forward Fill missing values (you can also use .fillna(), as shown below)
    # inner_merged_df.fillna(value="NaN", inplace=True)

    # Data preprocessing: Convert start_date and end_date to datetime
    # inner_merged_df["created_at"] = pd.to_datetime(inner_merged_df["expires_at"], errors="coerce")
    # inner_merged_df["expires_at"] = pd.to_datetime(inner_merged_df["expires_at"], errors="coerce")

    # Feature engineering
    # course_duration = inner_merged_df["end_date"] - inner_merged_df["start_date"]
    # inner_merged_df["course_duration"] = course_duration.dt.days
    # day_which_ticket_was_booked = datetime.strptime()

    # Describe the merged dataset
    # print("Summary Statistics:")
    # print(inner_merged_df.describe(include='all'))
    # print("\nColumn Info:")
    # print(inner_merged_df.info())
    # print("\nFirst Few Rows:")
    # print(inner_merged_df.head())
    # print("Null Values in Each Column:")
    # print(inner_merged_df.isnull().sum())
    # # Fill numeric NaN values with the mean of the respective columns
    # inner_merged_df.fillna(inner_merged_df.mean(numeric_only=True), inplace=True)
    # print("\nNull Values After Replacement:")
    # print(inner_merged_df.isnull().sum())
    # # Fill categorical NaN values with 'Unknown'
    # categorical_columns = inner_merged_df.select_dtypes(include=['object']).columns
    # inner_merged_df[categorical_columns] = inner_merged_df[categorical_columns].fillna('NAN')
    # print("\nNull Values After Replacement in Categorical Columns:")
    # print(inner_merged_df.isnull().sum())

    # Example for filling specific columns (e.g., 'column_name')
    # inner_merged_df['column_name'] = inner_merged_df['column_name'].fillna('Default Value')  # Replace with your column name
    # print("\nUpdated Dataset:")
    # print(inner_merged_df)

    # Drop rows with any remaining NaN values
    # inner_merged_df = inner_merged_df.dropna()
    # Drop columns with NaN values
    # inner_merged_df = inner_merged_df.dropna(axis=1)
    # print("\nDataset After Dropping Nulls:")
    # print(inner_merged_df)

    # Check for duplicate rows
    # duplicates = inner_merged_df[inner_merged_df.duplicated()]
    # print(f"Number of duplicate rows: {len(duplicates)}")
    # print(duplicates)
    # Drop duplicate rows
    # inner_merged_df = inner_merged_df.drop_duplicates()
    # print("Duplicate rows removed.")
    # print(f"Dataset shape after removing duplicates: {inner_merged_df.shape}")

    # # Drop duplicates based on specific columns
    # inner_merged_df = inner_merged_df.drop_duplicates(subset=['name'])
    # print("Duplicates based on specific columns removed.")
    # print(f"Dataset shape after removing duplicates: {inner_merged_df.shape}")
    # # Add a flag for duplicates
    # inner_merged_df['is_duplicate'] = inner_merged_df.duplicated()
    # print("Dataset with duplicate flag:")
    # print(inner_merged_df)
    # # Separate duplicate rows
    # duplicate_rows = inner_merged_df[inner_merged_df.duplicated()]
    # print("Duplicate rows:")
    # print(duplicate_rows)
    # Aggregate duplicate rows by summing values in numerical columns
    # inner_merged_df = inner_merged_df.groupby(['column_name']).agg('sum').reset_index()
    # # Save the cleaned dataset
    # inner_merged_df.to_csv('cleaned_dataset.csv', index=False)
    # print("Cleaned dataset saved as 'cleaned_dataset.csv'")
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")