import streamlit as st
import faiss
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from io import StringIO
import chardet
from PyPDF2 import PdfReader
from docx import Document
from datetime import datetime
import csv

# Define the retriever class
class LightRAGRetriever:
    def __init__(self):
        self.documents = []
        self.embeddings = None
        self.index = None
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Semantic search model

    def build_index(self, documents):
        self.documents = documents
        self.embeddings = self.model.encode(documents, convert_to_tensor=True)
        faiss.normalize_L2(np.array(self.embeddings, dtype=np.float32))  # Normalize embeddings for cosine similarity
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(np.array(self.embeddings, dtype=np.float32))

    def retrieve(self, query, top_k=5):
        if not self.index:
            return [("No documents uploaded yet.", 0.0)]
        query_embedding = self.model.encode([query], convert_to_tensor=True).detach().numpy()
        distances, indices = self.index.search(np.array(query_embedding, dtype=np.float32), top_k)
        return [(self.documents[idx], distances[0][i]) for i, idx in enumerate(indices[0])]

# Define the generator class
class LightRAGGenerator:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def generate(self, context, query, max_length=150):
        input_text = f"{query}\n{context}"
        inputs = self.tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.model.generate(inputs, max_length=max_length, num_beams=5, early_stopping=True)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# Function to process uploaded files
def process_uploaded_file(uploaded_file):
    try:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            text = "".join(page.extract_text() or "" for page in reader.pages)
            return text
        elif uploaded_file.type == "text/plain":
            raw_data = uploaded_file.getvalue()
            detected_encoding = chardet.detect(raw_data)['encoding']
            return raw_data.decode(detected_encoding, errors="replace")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            return "\n".join(para.text for para in doc.paragraphs)
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
            df = pd.read_excel(uploaded_file)
            return df.to_csv(index=False)
        else:
            raise ValueError(f"Unsupported file type: {uploaded_file.type}")
    except Exception as e:
        raise ValueError(f"Error processing file: {e}")

# Streamlit App
def main():
    st.set_page_config(page_title="LightRAG Chatbot", layout="wide", page_icon="🤖")

    # Header Section
    st.markdown("""
        <style>
            .main-header {
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
            }
            .sub-header {
                font-size: 20px;
                text-align: center;
                color: #555;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="main-header">LightRAG Chatbot 🤖 </div>', unsafe_allow_html=True)
    #st.markdown('<div class="sub-header">Upload documents (PDF, text, Word, or Excel) and interact with a chatbot to get intelligent responses.</div>', unsafe_allow_html=True)

    # Initialize retriever and generator
    retriever = LightRAGRetriever()
    generator = LightRAGGenerator()

    # Sidebar options
    with st.sidebar:
        st.header("⚙️ Configuration")
        top_k = st.slider("Number of documents to retrieve:", 1, 10, 3)
        response_length = st.slider("Max response length (words):", 50, 300, 150)

    # File uploader
    st.subheader("📂 Upload Your Documents")
    uploaded_files = st.file_uploader("Upload text, PDF, Word, or Excel documents:",
                                      type=["txt", "pdf", "docx", "xlsx", "xls"],
                                      accept_multiple_files=True)

    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            try:
                document_text = process_uploaded_file(uploaded_file)
                if document_text.strip():
                    documents.append(document_text)
                    st.success(f"Successfully processed: {uploaded_file.name}")
                else:
                    st.warning(f"{uploaded_file.name} contains no extractable text.")
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")

        if documents:
            retriever.build_index(documents)
            st.success(f"{len(documents)} document(s) uploaded and indexed successfully!")

    # Initialize the chat history if not already initialized
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Chat Interface
    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("💬 Ask Your Query")
        user_query = st.text_input("Enter your query:", placeholder="Enter your query here...")
        submit_query = st.button("Submit Query", type="primary")

        if submit_query and user_query:
            if retriever.documents:
                retrieved_docs = retriever.retrieve(user_query, top_k=top_k)
                context = " ".join([doc[:512] for doc, _ in retrieved_docs])  # Ensure context fits the token limit
                response = generator.generate(context, user_query, max_length=response_length)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.chat_history.append({"user": user_query, "bot": response, "time": timestamp})
                st.subheader("🤖 Chatbot Response")
                st.write(response)

                with st.expander("🔍 Retrieved Documents"):
                    for i, (doc, score) in enumerate(retrieved_docs):
                        st.markdown(f"**Document {i + 1} (Score: {score:.4f}):**")
                        st.write(doc[:500] + ("..." if len(doc) > 500 else ""))
            else:
                st.warning("Please upload documents before asking a query.")

    with col2:
        st.subheader("🕒 Chat History")
        st.markdown('<div class="chat-history">', unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            user_msg = f"""
            <div style="background-color:#E0E0E0;padding:10px;border-radius:15px;margin-bottom:10px;max-width:90%;">
                <strong>User:</strong> <span style="font-size:0.8em;color:gray;">({chat['time']})</span><br>{chat['user']}
            </div>
            """
            bot_msg = f"""
            <div style="background-color:#A5D6A7;padding:10px;border-radius:15px;margin-bottom:10px;max-width:90%;">
                <strong>Bot:</strong> <span style="font-size:0.8em;color:gray;">({chat['time']})</span><br>{chat['bot']}
            </div>
            """
            st.markdown(user_msg, unsafe_allow_html=True)
            st.markdown(bot_msg, unsafe_allow_html=True)


    # Raise a Ticket Section
    # Raise a Ticket Section
    st.markdown("---")
    st.subheader("📩 Issue Reporting")

    if st.button("Raise a Ticket"):
        with st.form("ticket_form", clear_on_submit=True):
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            email_address = st.text_input("Email Address", placeholder="Enter your email address")
            issue_description = st.text_area("Describe Your Issue", placeholder="Please describe the issue in detail")
            submit_ticket = st.form_submit_button("Submit Ticket")

            if submit_ticket:
                # Save ticket information to a CSV file
                ticket_data = {
                    "Full Name": full_name,
                    "Email Address": email_address,
                    "Issue Description": issue_description
                }
                
                with open("tickets.csv", mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["Full Name", "Email Address", "Issue Description"])
                    
                    # Write header only if the file is new/empty
                    if file.tell() == 0:
                        writer.writeheader()
                    
                    writer.writerow(ticket_data)
                
                st.success("✅ Your ticket has been successfully submitted. Our team will reach out to you shortly!")

if __name__ == "__main__":
    main()
