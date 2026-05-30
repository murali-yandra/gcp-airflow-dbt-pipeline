import os
import pandas as pd
from google.cloud import storage

# 1. THE AUTHENTICATION HANDSHAKE
# We tell the Google Cloud SDK exactly where to find our "robot badge"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_key.json"

def upload_to_gcs():
    # Replace this with the exact name of the bucket you just created
    bucket_name = "faang-data-lake-murali-yandra"
    local_file_name = "sample_products.csv"
    
    # 2. Create a local dataset to test the upload
    print("Generating local CSV file...")
    df = pd.DataFrame({
        "product_id": [101, 102, 103],
        "product_name": ["Mechanical Keyboard", "Wireless Mouse", "Ultra-wide Monitor"],
        "price_usd": [120.00, 45.50, 399.99]
    })
    df.to_csv(local_file_name, index=False)
    
    # 3. Connect to the Cloud Data Lake
    print("Authenticating with Google Cloud...")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    # 4. Define the destination path in the cloud
    # 'blob' is the cloud name for your file. We are putting it inside a 'raw/' folder.
    destination_blob_name = f"raw/{local_file_name}"
    blob = bucket.blob(destination_blob_name)
    
    # 5. Execute the upload
    print(f"Uploading {local_file_name} to GCP...")
    blob.upload_from_filename(local_file_name)
    
    print(f"SUCCESS: File securely landed in gs://{bucket_name}/{destination_blob_name}")

if __name__ == "__main__":
    upload_to_gcs()