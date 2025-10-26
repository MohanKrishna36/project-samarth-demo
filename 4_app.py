import os
import sys
import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import google.generativeai as genai

# ONE place for set_page_config - at the very top after imports-only
st.set_page_config(
    page_title="Project Samarth - AgriClimate Q&A",
    page_icon="🌾",
    layout="wide"
)

# Paths for checking vectorstore existence
VECTOR_FAISS_PATH = "vectorstore/index.faiss"
VECTOR_PKL_PATH = "vectorstore/index.pkl"
if not (os.path.exists(VECTOR_FAISS_PATH) and os.path.exists(VECTOR_PKL_PATH)):
    with st.spinner("First-time setup: Downloading, cleaning, and indexing data from data.gov.in. This may take several minutes..."):
        result1 = os.system(f"{sys.executable} 1_download_data.py")
        result2 = os.system(f"{sys.executable} 2_clean_data.py")
        result3 = os.system(f"{sys.executable} 3_build_vectorstore.py")
    if not (os.path.exists(VECTOR_FAISS_PATH) and os.path.exists(VECTOR_PKL_PATH)):
        st.error("❌ Vector DB could not be built automatically. No data found or error occurred. Please check scripts and API key or report an issue.")
        st.stop()

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore

def get_answer(question, vectorstore):
    docs = vectorstore.similarity_search(question, k=5)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""You are an intelligent assistant analyzing Indian agricultural and climate data from data.gov.in.

Use the following context to answer the question accurately.

IMPORTANT INSTRUCTIONS:
- Provide specific numbers and statistics from the data
- Always cite the source (state, district, year, subdivision) for each data point
- If comparing regions, present data in a clear format
- If data is unavailable, clearly state that
- Be precise and factual

Context from data.gov.in:
{context}

Question: {question}

Detailed Answer with Citations:"""
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text, docs

def main():
    st.title("🌾 Project Samarth")
    st.caption("Agricultural & Climate Intelligence Q&A System powered by data.gov.in")

    with st.sidebar:
        st.header("📊 About")
        st.write("This system answers questions about India's agricultural economy and climate patterns using official government data.")
        st.subheader("Data Sources:")
        st.write("✅ Ministry of Agriculture & Farmers Welfare")
        st.write("✅ India Meteorological Department (IMD)")
        st.subheader("Sample Questions:")
        st.write("- What crops are in the data?")
        st.write("- What was the production of rice in GUNTUR district, Andhra Pradesh in 2004?")
        st.write("- Show the pattern of sugarcane production in SUPAUL, Bihar from 2010 to 2014")
        st.write("- Tell me about rainfall patterns")
        st.write("- What is the rice production?")

    if not os.getenv('GOOGLE_API_KEY'):
        st.error("❌ Google API key not found. Please add it to .env file or Streamlit Cloud secrets!")
        return

    try:
        with st.spinner("Loading Q&A system..."):
            vectorstore = load_vectorstore()
        st.success("✅ System ready!")
    except Exception as e:
        st.error(f"❌ Error loading system: {e}")
        return

    st.subheader("💬 Ask Your Question")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("Ask about crops, rainfall, or agricultural trends..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing data from data.gov.in..."):
                try:
                    response, sources = get_answer(prompt, vectorstore)
                    st.markdown(response)
                    with st.expander("📚 View Data Sources"):
                        st.write(f"Retrieved {len(sources)} relevant data points:")
                        for i, doc in enumerate(sources, 1):
                            st.markdown(f"**Source {i}:**")
                            st.json(doc.metadata)
                            st.divider()
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error generating response: {e}")

if __name__ == "__main__":
    main()
