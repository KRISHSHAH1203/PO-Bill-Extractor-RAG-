import os
import tempfile
import uuid
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from openai import OpenAI
from backend.po_model import POBillData
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

class OpenRouterEmbeddings(OpenAIEmbeddings):
    """Custom embeddings client including OpenRouter HTTP-Referer header."""

    def _create_client(self) -> OpenAI:
        return OpenAI(
            api_key=self.openai_api_key,
            base_url=self.openai_api_base,
            # Make sure this matches your Streamlit app URL
            extra_headers={"HTTP-Referer": "http://localhost:8501"},
        )

class OpenRouterChatOpenAI(ChatOpenAI):
    """Custom chat client including OpenRouter HTTP-Referer header."""

    def _create_client(self) -> OpenAI:
        return OpenAI(
            api_key=self.openai_api_key,
            base_url=self.openai_api_base,
            extra_headers={"HTTP-Referer": "http://localhost:8501"},
        )

def get_pdf_text(uploaded_file):
    """Extract documents from uploaded PDF file."""
    input_file = uploaded_file.read()
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(input_file)
    temp_file.close()
    loader = PyPDFLoader(temp_file.name)
    documents = loader.load()
    os.unlink(temp_file.name)
    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=100):
    """Split documents into smaller chunks for vector embedding."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

def get_embeddings():
    """Instantiate OpenRouter embeddings model with headers."""
    # return OpenRouterEmbeddings(
    #     model="text-embedding-3-small",
    #     openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    #     openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
    # )
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def clean_filename(filename):
    """Sanitize filenames to valid Chroma collection names."""
    name = filename.lower()
    name = re.sub(r'\.pdf$', '', name)          # remove .pdf extension
    name = re.sub(r'[^a-z0-9._-]', '-', name)  # replace invalid chars with dash
    name = re.sub(r'-+', '-', name)             # collapse multiple dashes
    name = name.strip('-._')                     # trim invalid chars at start/end
    if len(name) < 3:
        name = (name + "collection")[:3]
    elif len(name) > 512:
        name = name[:512]
    return name

def create_vectorstore(docs, file_name):
    """Create or load a Chroma vectorstore from docs and filename."""
    ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in docs]
    return Chroma.from_documents(
        docs,
        collection_name=clean_filename(file_name),
        embedding=get_embeddings(),
        ids=ids,
        persist_directory="db",
    )

PROMPT_TEMPLATE = """
You are a world-class invoice and purchase order document extractor.

Extract the following structured data from the context below:

- PO number
- PO date
- Vendor name, address, contact
- Buyer name, address, contact
- Shipping address
- Billing address
- Line items (name, description, quantity, unit price, total price)
- Subtotal
- Tax
- Total amount
- Terms & Conditions

If something is not present, output null. Respond in correct JSON format.

{format_instructions}

Context:
{context}
"""

def extract_po_data(vectorstore):
    """Use the vectorstore to retrieve context and extract structured PO data using GPT-5."""
    retriever = vectorstore.as_retriever()
    docs = retriever.invoke("Extract all details from this purchase order")
    context = "\n\n".join(doc.page_content for doc in docs)

    llm = OpenRouterChatOpenAI(
        model="openai/gpt-oss-20b", 
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL"),
    )

    parser = PydanticOutputParser(pydantic_object=POBillData)

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "format_instructions"],
    )

    chain = prompt | llm

    llm_output = chain.invoke(
        {
            "context": context,
            "format_instructions": parser.get_format_instructions(),
        }
    )

    output = parser.parse(llm_output.content)
    return output