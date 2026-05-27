import requests
import pandas as pd
from sqlalchemy import create_engine

def extract_transform_load():
    # 1. EXTRACT: Talk to the API using Pagination
    print("Fetching live data from API with Pagination...")
    
    all_products = []
    skip = 0
    limit = 30
    
    # We create an infinite loop that only stops when the API returns an empty list
    while True:
        # We pass parameters into the URL to tell the API which 'page' we want
        url = f"https://dummyjson.com/products?limit={limit}&skip={skip}"
        response = requests.get(url)
        raw_json = response.json() 
        
        products = raw_json.get('products', [])
        
        # Guard clause: If the list is empty, we've collected everything. Break the loop.
        if len(products) == 0:
            break
            
        all_products.extend(products) # Add this batch to our master list
        skip += limit # Increase the skip counter to get the next page on the next loop
        
        print(f"Extracted a batch of {len(products)}. Total so far: {len(all_products)}")

    # 2. TRANSFORM: Convert JSON into a structured table
    df = pd.DataFrame(all_products)
    df = df[['id', 'title', 'price', 'stock']]
    df['price'] = df['price'].astype(float)
    
    print(f"Transformed {len(df)} rows. Preparing to load...")

    # 3. LOAD: Push data to Dockerized PostgreSQL
    print("Connecting to local PostgreSQL database...")
    engine = create_engine('postgresql://admin:password123@postgres_db:5432/data_warehouse')
    
    df.to_sql('products_raw', engine, if_exists='replace', index=False)
    
    print("SUCCESS: Pipeline complete. All paginated data loaded into PostgreSQL.")

if __name__ == "__main__":
    extract_transform_load()