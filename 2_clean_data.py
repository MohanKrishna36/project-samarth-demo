"""
Step 2: Clean and Prepare Data
UPDATED: Handle larger datasets efficiently
"""
import pandas as pd
import os

def clean_crop_data():
    """Clean crop production data (optimized for large dataset)"""
    
    print("\n" + "="*60)
    print("Cleaning Crop Production Data")
    print("="*60)
    
    # Load data
    print("Loading crop data...")
    df = pd.read_csv('data/agriculture/crop_production.csv')
    
    print(f"Original records: {len(df):,}")
    print(f"Columns: {list(df.columns)}")
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    
    # Identify critical columns
    critical_cols = []
    for col in ['state_name', 'district_name', 'crop_year', 'season', 'crop', 'area_', 'production_']:
        if col in df.columns:
            critical_cols.append(col)
    
    # Remove rows with missing critical data
    before = len(df)
    if critical_cols:
        df = df.dropna(subset=critical_cols)
    after = len(df)
    print(f"Removed {before - after:,} rows with missing data")
    
    # Remove aggregate/total rows
    if 'district_name' in df.columns:
        df = df[~df['district_name'].str.lower().str.contains('total', na=False)]
        print(f"Removed aggregate rows")
    
    # Convert numeric columns
    for col in ['area_', 'production_', 'crop_year']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove rows with zero or negative production
    if 'production_' in df.columns:
        before = len(df)
        df = df[df['production_'] > 0]
        print(f"Removed {before - len(df):,} rows with zero/negative production")
    
    # Remove rows with zero area
    if 'area_' in df.columns:
        before = len(df)
        df = df[df['area_'] > 0]
        print(f"Removed {before - len(df):,} rows with zero area")
    
    # Save cleaned data
    os.makedirs('processed_data', exist_ok=True)
    df.to_csv('processed_data/crop_data_cleaned.csv', index=False)
    
    print(f"\n✅ Cleaned crop data: {len(df):,} records")
    print(f"   Saved to: processed_data/crop_data_cleaned.csv")
    
    if 'state_name' in df.columns:
        print(f"   States: {df['state_name'].nunique()}")
        print(f"   Top 5 states: {df['state_name'].value_counts().head().index.tolist()}")
    if 'crop' in df.columns:
        print(f"   Crops: {df['crop'].nunique()}")
        print(f"   Top 5 crops: {df['crop'].value_counts().head().index.tolist()}")
    if 'crop_year' in df.columns:
        print(f"   Years: {int(df['crop_year'].min())} to {int(df['crop_year'].max())}")
    
    return df

def clean_rainfall_data():
    """Clean rainfall data (optimized for larger dataset)"""
    
    print("\n" + "="*60)
    print("Cleaning Rainfall Data")
    print("="*60)
    
    # Load data
    print("Loading rainfall data...")
    df = pd.read_csv('data/climate/rainfall.csv')
    
    print(f"Original records: {len(df):,}")
    print(f"Columns: {list(df.columns)}")
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()
    
    # Remove rows with missing subdivision or year
    before = len(df)
    df = df.dropna(subset=['subdivision', 'year'])
    print(f"Removed {before - len(df):,} rows with missing subdivision/year")
    
    # Convert year to integer
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df.dropna(subset=['year'])
    df['year'] = df['year'].astype(int)
    
    # Save cleaned data
    df.to_csv('processed_data/rainfall_data_cleaned.csv', index=False)
    
    print(f"\n✅ Cleaned rainfall data: {len(df):,} records")
    print(f"   Saved to: processed_data/rainfall_data_cleaned.csv")
    print(f"   Subdivisions: {df['subdivision'].nunique()}")
    print(f"   Top 5 subdivisions: {df['subdivision'].value_counts().head().index.tolist()}")
    print(f"   Years: {int(df['year'].min())} to {int(df['year'].max())}")
    
    return df

def main():
    print("\n" + "="*60)
    print("PROJECT SAMARTH - DATA CLEANING")
    print("="*60)
    
    # Check if data exists
    if not os.path.exists('data/agriculture/crop_production.csv'):
        print("\n❌ ERROR: Run 1_download_data.py first!")
        return
    
    # Clean crop data
    crop_df = clean_crop_data()
    
    # Clean rainfall data
    rain_df = clean_rainfall_data()
    
    print("\n" + "="*60)
    print("✅ DATA CLEANING COMPLETE!")
    print("="*60)
    print(f"\nTotal cleaned records: {len(crop_df) + len(rain_df):,}")
    print("\nNext: Run python 3_build_vectorstore.py")

if __name__ == "__main__":
    main()

