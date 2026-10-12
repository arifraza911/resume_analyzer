from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings


load_dotenv()


# Embedding model
embeddings = MistralAIEmbeddings(
    model="mistral-embed"
)


# Load PDF
loader = PyPDFLoader(
    "./aarif_resume.pdf"
)

documents = loader.load()


# Split PDF into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)


# Create ChromaDB
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="../pdf_analyzer_db"
)


# Add PDF chunks to database
vector_store.add_documents(
    documents=chunks
)

print("Database created successfully!")