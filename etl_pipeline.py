import requests
import pandas as pd
from sqlalchemy import create_engine

def extract_transform_load():
    # 1. EXTRACT: Talk to the API
    url = "https://dummyjson.com/products"
    print("Fetching live data from API...")
    
    response = requests.get(url)
    raw_json = response.json() 

    # 2. TRANSFORM: Convert JSON into a structured table
    df = pd.DataFrame(raw_json['products'])
    df = df[['id', 'title', 'price', 'stock']]
    df['price'] = df['price'].astype(float)
    
    print(f"Transformed {len(df)} rows. Preparing to load...")

    # 3. LOAD: Push data to Dockerized PostgreSQL
    # Connection String Format: dialect://username:password@host:port/database
    print("Connecting to local PostgreSQL database...")
    engine = create_engine('postgresql://admin:password123@localhost:5432/data_warehouse')
    
    # Automatically create a table called 'products_raw' and insert the data
    # if_exists='replace' means it will drop and recreate the table if we run this script twice
    df.to_sql('products_raw', engine, if_exists='replace', index=False)
    
    print("SUCCESS: Pipeline complete. Data loaded into PostgreSQL.")

if __name__ == "__main__":
    extract_transform_load()