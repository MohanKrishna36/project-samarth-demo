"""
Step 3: Build Vector Database
Updated for REAL crop production dataset
"""
import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
import os

def create_documents_from_crop_data():
    """Convert crop data to text documents (UPDATED FORMAT)"""
    
    print("\n" + "="*60)
    print("Creating documents from crop data...")
    print("="*60)
    
    df = pd.read_csv('processed_data/crop_data_cleaned.csv')
    
    documents = []
    
    for idx, row in df.iterrows():
        # Create readable text from data (NEW FIELDS)
        text = f"""
Agricultural Production Data:
State: {row.get('state_name', 'N/A')}
District: {row.get('district_name', 'N/A')}
Crop: {row.get('crop', 'N/A')}
Season: {row.get('season', 'N/A')}
Year: {row.get('crop_year', 'N/A')}
Area: {row.get('area_', 0)} hectares
Production: {row.get('production_', 0)} tonnes
Yield: {row.get('production_', 0) / row.get('area_', 1) if row.get('area_', 0) > 0 else 0:.2f} tonnes/hectare
Source: Ministry of Agriculture, data.gov.in
        """
        
        metadata = {
            'source': 'crop_production',
            'state': str(row.get('state_name', 'N/A')),
            'district': str(row.get('district_name', 'N/A')),
            'crop': str(row.get('crop', 'N/A')),
            'year': str(row.get('crop_year', 'N/A')),
            'season': str(row.get('season', 'N/A'))
        }
        
        documents.append(Document(page_content=text, metadata=metadata))
        
        if (idx + 1) % 500 == 0:
            print(f"  Processed {idx + 1} records...")
    
    print(f"✅ Created {len(documents)} crop documents")
    return documents

def create_documents_from_rainfall_data():
    """Convert rainfall data to text documents"""
    
    print("\n" + "="*60)
    print("Creating documents from rainfall data...")
    print("="*60)
    
    df = pd.read_csv('processed_data/rainfall_data_cleaned.csv')
    
    documents = []
    
    for idx, row in df.iterrows():
        # Create readable text from data
        text = f"""
Climate Data - Rainfall:
Subdivision: {row.get('subdivision', 'N/A')}
Year: {row.get('year', 'N/A')}
January: {row.get('jan', 0)} mm
February: {row.get('feb', 0)} mm
March: {row.get('mar', 0)} mm
April: {row.get('apr', 0)} mm
May: {row.get('may', 0)} mm
June: {row.get('jun', 0)} mm
July: {row.get('jul', 0)} mm
August: {row.get('aug', 0)} mm
September: {row.get('sep', 0)} mm
October: {row.get('oct', 0)} mm
November: {row.get('nov', 0)} mm
December: {row.get('dec', 0)} mm
Annual Total: {row.get('annual', 0)} mm
Source: India Meteorological Department, data.gov.in
        """
        
        metadata = {
            'source': 'rainfall',
            'subdivision': str(row.get('subdivision', 'N/A')),
            'year': str(row.get('year', 'N/A'))
        }
        
        documents.append(Document(page_content=text, metadata=metadata))
        
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1} records...")
    
    print(f"✅ Created {len(documents)} rainfall documents")
    return documents

def build_vectorstore(documents):
    """Create FAISS vector store from documents"""
    
    print("\n" + "="*60)
    print("Building vector database...")
    print("="*60)
    
    # Create embeddings
    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    print("✅ Embedding model loaded")
    
    # Create vector store
    print("Creating vector store (this may take a few minutes)...")
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Save vector store
    os.makedirs('vectorstore', exist_ok=True)
    vectorstore.save_local("vectorstore")
    
    print("✅ Vector store saved to: vectorstore/")
    
    return vectorstore

def main():
    print("\n" + "="*60)
    print("PROJECT SAMARTH - BUILD VECTOR DATABASE (UPDATED)")
    print("="*60)
    
    # Check if cleaned data exists
    if not os.path.exists('processed_data/crop_data_cleaned.csv'):
        print("\n❌ ERROR: Run 2_clean_data.py first!")
        return
    
    # Create documents
    crop_docs = create_documents_from_crop_data()
    rain_docs = create_documents_from_rainfall_data()
    
    # Combine all documents
    all_documents = crop_docs + rain_docs
    print(f"\n📊 Total documents: {len(all_documents)}")
    
    # Build vector store
    vectorstore = build_vectorstore(all_documents)
    
    print("\n" + "="*60)
    print("✅ VECTOR DATABASE COMPLETE!")
    print("="*60)
    print(f"\nStored {len(all_documents)} documents")
    print("\nNext: Run streamlit run 4_app.py")

if __name__ == "__main__":
    main()
