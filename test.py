import pandas as pd
import time

def read_and_time_feather(file_path):
    start_time = time.time()
    df = pd.read_feather(file_path)
    end_time = time.time()
    print(f"Feather file loaded in {end_time - start_time:.4f} seconds")
    return df

def read_and_time_pickle(file_path):
    start_time = time.time()
    df = pd.read_pickle(file_path)
    end_time = time.time()
    print(f"Pickle file loaded in {end_time - start_time:.4f} seconds")
    return df

if __name__ == '__main__':
    feather_file = 'data/combined_data.feather'
    pickle_file = 'data/combined_data.pkl'

    print("Reading Feather file:")
    df_feather = read_and_time_feather(feather_file)
    print(df_feather.head())

    print("\nReading Pickle file:")
    df_pickle = read_and_time_pickle(pickle_file)
    print(df_pickle.head())
