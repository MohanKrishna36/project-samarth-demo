"""
Step 1: Download Data from data.gov.in
UPDATED: Download MORE data for comprehensive coverage
- 50,000 crop records (multiple states, districts, years)
- 10,000 rainfall records (comprehensive climate data)
"""
import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time

# Load your API key
load_dotenv()
API_KEY = os.getenv('DATA_GOV_API_KEY')

# Dataset Resource IDs - VERIFIED WORKING
DATASETS = {
    "crop_production": "35be999b-0208-4354-b557-f6ca9a5355de",  # Real district-wise data
    "rainfall": "8e0bd482-4aba-4d99-9cb9-ff124f6f1c2f"  # IMD rainfall data
}

def download_dataset(resource_id, dataset_name, limit=10000):
    """Download dataset from data.gov.in with progress tracking"""
    
    print(f"\n{'='*60}")
    print(f"Downloading: {dataset_name}")
    print(f"Target: {limit} records")
    print(f"{'='*60}")
    
    url = f"https://api.data.gov.in/resource/{resource_id}"
    
    all_records = []
    offset = 0
    batch_size = 100
    
    while offset < limit:
        params = {
            "api-key": API_KEY,
            "format": "json",
            "offset": offset,
            "limit": batch_size
        }
        
        print(f"Fetching records {offset} to {offset+batch_size}... ", end='')
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'records' in data and len(data['records']) > 0:
                    all_records.extend(data['records'])
                    print(f"✓ Got {len(data['records'])} records")
                    offset += batch_size
                    
                    # Small delay to avoid rate limiting
                    time.sleep(0.5)
                else:
                    print("No more records available.")
                    break
            else:
                print(f"Error: HTTP {response.status_code}")
                break
                
        except Exception as e:
            print(f"Error: {e}")
            break
    
    if all_records:
        df = pd.DataFrame(all_records)
        
        # Create folder
        folder = 'data/agriculture' if 'crop' in dataset_name.lower() else 'data/climate'
        os.makedirs(folder, exist_ok=True)
        
        # Save
        filename = f"{folder}/{dataset_name.replace(' ', '_').lower()}.csv"
        df.to_csv(filename, index=False)
        
        print(f"\n✅ SUCCESS!")
        print(f"   Records downloaded: {len(df)}")
        print(f"   Saved to: {filename}")
        print(f"   File size: {os.path.getsize(filename) / (1024*1024):.2f} MB")
        
        # Show sample of what we got
        if 'state_name' in df.columns:
            print(f"   States: {df['state_name'].nunique()}")
            print(f"   Sample states: {df['state_name'].unique()[:5].tolist()}")
        if 'crop' in df.columns:
            print(f"   Crops: {df['crop'].nunique()}")
            print(f"   Sample crops: {df['crop'].unique()[:5].tolist()}")
        if 'crop_year' in df.columns:
            print(f"   Years: {df['crop_year'].min()} to {df['crop_year'].max()}")
        if 'subdivision' in df.columns:
            print(f"   Subdivisions: {df['subdivision'].nunique()}")
            print(f"   Sample: {df['subdivision'].unique()[:5].tolist()}")
        if 'year' in df.columns:
            print(f"   Years: {df['year'].min()} to {df['year'].max()}")
        
        return df
    else:
        print("\n❌ No data downloaded")
        return None

def main():
    print("\n" + "="*60)
    print("PROJECT SAMARTH - COMPREHENSIVE DATA DOWNLOAD")
    print("="*60)
    
    # Check API key
    if not API_KEY or API_KEY == 'your_key_here':
        print("\n❌ ERROR: Add your API key to .env file")
        return
    
    print(f"\n✓ API Key found: {API_KEY[:20]}...")
    print("\n⚠️  This will take 15-20 minutes. Please be patient!")
    
    start_time = time.time()
    
    # Download crop production data - GET 50,000 RECORDS
    print("\n[1/2] Downloading Crop Production Data...")
    print("This will give us multiple states, districts, and years")
    crop_df = download_dataset(
        DATASETS["crop_production"], 
        "crop_production",
        limit=50000  # 50K records for comprehensive coverage
    )
    
    # Download rainfall data - GET 10,000 RECORDS
    print("\n[2/2] Downloading Rainfall Data...")
    print("This will give us comprehensive climate patterns")
    rain_df = download_dataset(
        DATASETS["rainfall"],
        "rainfall",
        limit=10000  # 10K records for better climate coverage
    )
    
    elapsed_time = time.time() - start_time
    
    print("\n" + "="*60)
    print("✅ DATA DOWNLOAD COMPLETE!")
    print("="*60)
    
    if crop_df is not None:
        print(f"\n📊 Crop Data: {len(crop_df):,} records")
        print(f"   Saved to: data/agriculture/crop_production.csv")
    
    if rain_df is not None:
        print(f"\n🌧️  Rainfall Data: {len(rain_df):,} records")
        print(f"   Saved to: data/climate/rainfall.csv")
    
    print(f"\n⏱️  Total time: {elapsed_time/60:.1f} minutes")
    print("\n✅ STEP 1 COMPLETE!")
    print("Next: Run python 2_clean_data.py")

if __name__ == "__main__":
    main()
