import streamlit as st
import json
import base64
from backend.extractor import get_pdf_text, split_documents, create_vectorstore, extract_po_data

# Streamlit page config
st.set_page_config(page_title="PO Bill Extractor", layout="wide")
st.title("📄 PO Bill Extractor")

# Upload the PDF file
uploaded_file = st.file_uploader("📤 Upload a PO/Bill PDF", type="pdf")

if uploaded_file:
    # Split the page into two columns
    col1, col2 = st.columns([1, 1])

    # Display PDF in left column
    with col1:
        st.markdown("### 🔍 Uploaded Document")
        bytes_data = uploaded_file.getvalue()
        base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    with st.spinner("🔄 Processing and extracting structured data..."):
        # Extract text from PDF
        documents = get_pdf_text(uploaded_file)

        # Split documents into chunks
        chunks = split_documents(documents)

        # Create vectorstore from chunks
        vectorstore = create_vectorstore(chunks, file_name=uploaded_file.name)

        # Use LLM to extract structured JSON
        po_data = extract_po_data(vectorstore)

    # Display and download JSON in right column
    with col2:
        st.markdown("### 📦 Extracted PO/Bill JSON")
        st.json(po_data.model_dump())

        # Prepare download button
        json_data = json.dumps(po_data.model_dump(), indent=2)
        st.download_button(
            label="📥 Download Extracted JSON",
            data=json_data,
            file_name="po_bill_data.json",
            mime="application/json"
        )
