# 📄 PO/Bill Extractor

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-orange)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A **real-world AI-powered PO/Bill extraction tool** that converts purchase orders and bills from PDF into **structured JSON** with high accuracy.  
It uses **LangChain**, **Retrieval-Augmented Generation (RAG)**, and **Pydantic** for robust parsing, with a **FastAPI backend** and **Streamlit frontend**.

---

## 🚀 Features

- 📄 **Extracts key fields**: vendor/buyer info, line items, addresses, totals, tax, and more  
- 🧠 **AI-powered parsing** using LangChain + embeddings (HuggingFace/OpenAI)  
- ⚡ **Fast & Accurate** – works with varied PDF layouts (tables, free-form text)  
- 🔐 **Secure API key handling** – keys stored on backend  
- 🖥 **Streamlit UI** with PDF preview and downloadable JSON output  
- 📦 **ERP-ready JSON** for easy integration  

---

## 📂 Tech Stack

- **Backend:** FastAPI, LangChain, OpenRouter/OpenAI APIs, HuggingFace embeddings  
- **Frontend:** Streamlit  
- **AI Model:** RAG pipeline with PydanticOutputParser  
- **Storage:** FAISS/Chroma Vector Store  
- **PDF Processing:** PyMuPDF (fitz), PyPDFLoader  

---

## 🛠 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/po-bill-extractor.git
cd po-bill-extractor
