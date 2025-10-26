# Project Samarth: Intelligent Q&A System for Indian Agriculture & Climate Data

## 🚀 Overview

**Project Samarth** is an end-to-end intelligent Q&A system that enables anyone to ask complex questions about India's agricultural production and climate trends, with all answers backed by live, official data from [data.gov.in](https://data.gov.in/).

**Key Technologies:**  
- **Streamlit (UI)**
- **LangChain (retrieval and LLM pipeline)**
- **FAISS (vectorstore for semantic search)**
- **Google Gemini (LLM for answer synthesis)**
- **Pandas, Python**

---

## 📈 Datasets Used

### 1. **Crop Production Data**
- **Source:** [data.gov.in District-wise, season-wise crop production statistics (from 1997)](https://data.gov.in/catalog/district-wise-season-wise-crop-production-statistics)
- **How obtained:** Automatically fetched via API using your unique DATA_GOV_API_KEY.
- **Schema:**
    - `state_name`, `district_name`
    - `crop_year`, `season`
    - `crop`
    - `area_` (hectares)
    - `production_` (tonnes)
- **Coverage:** Multiple states (Andhra Pradesh, Assam, Bihar, Chhattisgarh, Arunachal Pradesh, etc.), years 1997–2014, dozens of crops and districts.

### 2. **Rainfall Data**
- **Source:** [data.gov.in IMD Subdivision Rainfall Data](https://data.gov.in/catalog/historical-daily-meteorological-data)
- **How obtained:** Via API with DATA_GOV_API_KEY.
- **Schema:**
    - `subdivision` (e.g. West Uttar Pradesh, Uttarakhand)
    - `year`
    - `jan` .. `dec`, `annual` (monthly/annual rainfall, mm)
- **Coverage:** 1901–2017, all major Indian meteorological subdivisions.

**➡️ Both datasets are fetched, processed, vectorized, and stored locally for rapid retrieval and answer generation.  
Large raw files are **not** pushed to GitHub—regenerate them by running download/clean scripts with your own API key.**

---

## 🏗️ Project Folder Structure

samarth/
├── data/ # Raw input data (API-generated, not tracked in git)
│ ├── agriculture/crop_production.csv
│ └── climate/rainfall.csv
├── processed_data/ # Cleaned, deduped data (not tracked in git)
├── vectorstore/ # FAISS vector DB (not tracked in git)
├── .gitignore
├── .env.example # TEMPLATE for your API keys
├── 1_download_data.py
├── 2_clean_data.py
├── 3_build_vectorstore.py
├── 4_app.py # Streamlit chatbot UI
├── requirements.txt
└── README.md


---

## ⚙️ Setup, Install, and Run

**1. Clone the repository**

git clone https://github.com/MohanKrishna36/project-samarth-demo.git
cd project-samarth-demo

text

**2. Install requirements**
python -m venv venv

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt

text

**3. Set up API keys**
- Copy `.env.example` to `.env` and fill in:
    - `DATA_GOV_API_KEY` (from data.gov.in, register/login to generate)
    - `GOOGLE_API_KEY` (from Google AI Studio, needed for Gemini)
    - `LLM_PROVIDER=gemini`

**4. Download and Prepare Data**
python 1_download_data.py
python 2_clean_data.py
python 3_build_vectorstore.py

text

**5. Launch the chatbot!**
streamlit run 4_app.py

text

---

## 🌟 Features

- **NLQ Chatbot**: Ask e.g. “Compare paddy production in Assam and Bihar for 2010” or “Show rainfall trends in Uttarakhand since 1970”
- **Full cross-domain Q&A:** Analyze, compare, reason about crops and weather
- **Automatic citations**: All answers link to records and sources
- **Self-contained/End-to-end**: Download, clean, vectorize, serve in just a few commands
- **Hackathon/judge ready**: Repo is clean. No large proprietary files, only code and templates.

---

## 📝 Example Usage

- “What was the rice production in Bihar in 2010?”
- “List top 5 crops by volume in Andhra Pradesh for 2004.”
- “Which district in Chhattisgarh had the highest wheat production in 2011?”
- “What was the rainfall in East Uttar Pradesh in 1910?”

*(Answers depend on available live API data.)*

---

## 🌐 Deploy to Streamlit Cloud

1. Push your repo to GitHub (already done!).
2. Deploy on https://share.streamlit.io, pick `4_app.py`.
3. Add API secrets from your `.env` in the Deploy Secret settings.
4. Share your deployed app’s live link!

---

## 🛡️ Security/Confidentiality

- **Never commit `.env` (with real keys), large data, or `venv` to git!** Use `.env.example`.
- GitHub repo contains only code, configs, and key templates.
- Judges/others fetch their own data live with their API key.

---

## 👤 Author

- Mohan Krishna


---

## 📜 License

MIT License · for hackathon submission and demonstration use

---

**Questions, PRs, or Issues? Open on GitHub!**
