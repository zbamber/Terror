# scripts/ingest_data.py
import kagglehub
import pandas as pd
import psycopg2
import os
import sys
from dotenv import load_dotenv
from psycopg2.extras import execute_values

load_dotenv()
DIRECT_DATABASE_URL = os.getenv('DIRECT_DATABASE_URL')
if not DIRECT_DATABASE_URL:
    raise ValueError("DIRECT_DATABASE_URL (with ?sslmode=require) not found in .env file.")

print("Downloading and reading data...")
try:
    dataset_path = kagglehub.dataset_download("START-UMD/gtd")
    csv_path = os.path.join(dataset_path, "globalterrorismdb_0718dist.csv")
    df = pd.read_csv(csv_path, encoding='latin-1', engine='python')
    print(f"Loaded {len(df)} records successfully.")
except Exception as e:
    print(f"A critical error occurred while loading data: {e}")
    sys.exit(1)

print("Cleaning and transforming data...")
try:
    columns_to_keep = {
        'iyear': 'year', 'imonth': 'month', 'iday': 'day', 'country_txt': 'country',
        'provstate': 'state', 'city': 'city', 'latitude': 'lat', 'longitude': 'lng',
        'summary': 'summary', 'attacktype1_txt': 'attackType', 'targtype1_txt': 'targetType',
        'gname': 'groupName', 'nkill': 'numKilled'
    }
    df_cleaned = df[list(columns_to_keep.keys())].rename(columns=columns_to_keep)
    df_cleaned = df_cleaned.dropna(subset=['lat', 'lng'])
    df_cleaned = df_cleaned[df_cleaned['month'] != 0]
    df_cleaned = df_cleaned[df_cleaned['day'] != 0]
    df_cleaned['numKilled'] = df_cleaned['numKilled'].fillna(0)
    df_cleaned['state'] = df_cleaned['state'].fillna('')
    print(f"Data cleaned. {len(df_cleaned)} records remaining.")
except Exception as e:
    print(f"An error occurred during data cleaning: {e}")
    sys.exit(1)

print("Connecting to cloud database...")
conn = None
try:
    conn = psycopg2.connect(DIRECT_DATABASE_URL)
    cur = conn.cursor()

    columns_for_db = [
        'year', 'month', 'day', 'country', 'state', 'city', 'lat', 'lng', 
        'summary', 'attackType', 'targetType', 'groupName', 'numKilled'
    ]
    data_to_insert = [tuple(x) for x in df_cleaned[columns_for_db].to_numpy()]

    insert_sql = """
        INSERT INTO "Attack" (year, month, day, country, state, city, lat, lng, summary, "attackType", "targetType", "groupName", "numKilled") 
        VALUES %s
    """
    
    batch_size = 500 # A safe batch size
    total_records = len(data_to_insert)
    
    print(f"Ingesting {total_records} records in batches of {batch_size}...")
    
    for i in range(0, total_records, batch_size):
        batch = data_to_insert[i : i + batch_size]
        execute_values(cur, insert_sql, batch)
        conn.commit()
        print(f"  - Batch {i // batch_size + 1} of {total_records // batch_size + 1} committed.")

except Exception as e:
    print(f"An error occurred during database ingestion: {e}")
    # If an error happens, roll back any partial transaction
    if conn:
        conn.rollback()
    sys.exit(1)
finally:
    if conn:
        cur.close()
        conn.close()
        print("Database connection closed.")