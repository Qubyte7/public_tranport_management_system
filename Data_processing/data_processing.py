import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# gloabal variables
CLIENT_CACHE_FILE_DATAFRAMES = "./data_screenshot/clients_cached_dataframes.csv"
BOOKEDTICKETS_CACHE_FILE_DATAFRAMES =  "./data_screenshot/bookedtickets_cached_dataframes.csv"
MERGED_CACHE_FILE_DATAFRAMES = "./data_screenshot/merged_cached_dataframes.csv"
PROCESSED_DATAFRAMES_FILE = "./data_screenshot/processed_dataframes.csv"
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

def merge_dataframes_nullvalue_replacement(dataframedata1, dataframedata2):
    if is_cache_valid(MERGED_CACHE_FILE_DATAFRAMES):
        print("Retriving cached merged data frames !")
        return pd.read_csv(MERGED_CACHE_FILE_DATAFRAMES)
    print("Merging data frames !")
    inner_merged_df = pd.merge(dataframedata1,dataframedata2,left_on='id', right_on='client_id', how='inner')
    inner_merged_df.to_csv(MERGED_CACHE_FILE_DATAFRAMES, index=False)
    return inner_merged_df

def process_mergedframes(merged_dataframes_file, PROCESSED_DATAFRAMES_FILE):
    # print("before","\n",merged_dataframes["created_at"])
    if is_cache_valid(PROCESSED_DATAFRAMES_FILE):
        print("Using cached processed dataframes ...")
        return pd.read_csv(PROCESSED_DATAFRAMES_FILE)
    # cheching for missing values and replacing them
    print("Checking for null values !")
    if merged_dataframes_file.isnull().values.any():  # Correctly checks if any null values exist
        merged_dataframes_file.fillna(value="NaN", inplace=True)
        print("Done with filling null data frames with NaN!")
    else:
        print("No missing values detected.")
    # data pre_processing
    print("date pre processing ! ... ")
    merged_dataframes_file["created_at"] = pd.to_datetime(merged_dataframes["expires_at"], errors="coerce")
    merged_dataframes_file["expires_at"] = pd.to_datetime(merged_dataframes["expires_at"], errors="coerce")
    print("done date reformation !")

    print("Feature engineering started ...")
    #  features engineering
    merged_dataframes_file["day"] = merged_dataframes["created_at"].dt.strftime('%A')
    print(" Feature engineering finished !")
    print(" saving new processed data frames !")
    # saving the processed dataframes
    merged_dataframes_file.to_csv(PROCESSED_DATAFRAMES_FILE, index=False)
    print(" file saved , thanks for you patience ! ")

    return merged_dataframes



try:
    clients_dataframes = get_or_create_dataframe_excel_file('http://127.0.0.1:8000/app/v1/clients',CLIENT_CACHE_FILE_DATAFRAMES)
    booked_tickets_dataframes = get_or_create_dataframe_excel_file('http://127.0.0.1:8000/app/v1/booked_tickets',BOOKEDTICKETS_CACHE_FILE_DATAFRAMES)
    print("check ON the data_screenshot directory.")
    # Fetch data from API


    # Check DataFrames
    print(clients_dataframes.describe())
    print(booked_tickets_dataframes.describe())
    print(clients_dataframes.columns)
    print(booked_tickets_dataframes.columns)

    # Merging datasets based on 'id' (adjust 'id' if needed)
    merged_dataframes = merge_dataframes_nullvalue_replacement(clients_dataframes,booked_tickets_dataframes)
    print("Done with merging data frames !")

    # Data preprocessing
    process_mergedframes(merged_dataframes, PROCESSED_DATAFRAMES_FILE)
    print("chech data_processing directory !")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")