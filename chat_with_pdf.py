import streamlit as st
import os
from openai import OpenAI
from os import environ

from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

import io
from pypdf import PdfReader

client = OpenAI(
	api_key=os.environ["API_KEY"],
	base_url="https://api.ai.it.cornell.edu",
)

model_id="openai.gpt-4o"
EMBED_MODEL = "openai.text-embedding-3-small"

# --- Function: splits a document into small overlapping chunks 
# and adds them (with unique IDs) to the Chroma vector collection ---
def collection_adder(collection, text, name = "doc.txt"):
    # Create a new Chroma database and embedding function
    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 150)
    chunks = splitter.split_text(text)
    
    collection.add(documents = chunks, ids = [f"{i}-{name}" for i in range(len(chunks))])
    
st.title("📝 File Q&A with OpenAI")
uploaded_files = st.file_uploader("Upload an article", type=("txt", "pdf"), accept_multiple_files=True)


if uploaded_files:
    # Initialize the Chroma collection and embedding function only once
    text = ""
    if "collection" not in st.session_state:
        ef = OpenAIEmbeddingFunction(
        model_name = EMBED_MODEL, 
        api_key = os.environ["API_KEY"],

        )
        db = chromadb.Client()
        try: db.delete_collection("docs")
        except Exception: pass
        st.session_state["collection"] = db.create_collection(name = "docs", embedding_function = ef)
        st.session_state["seen"] = set()


    # process each of the uploaded files

    for f in uploaded_files:
        name = f.name.lower()
        seen = st.session_state["seen"]
        if name in seen:
            continue
        
        col = st.session_state["collection"]
        if name.endswith(".txt"):
            text = f.read().decode("utf-8", errors="ignore")
        elif name.endswith(".pdf"):
            data = io.BytesIO(f.read())
            pdf = PdfReader(data)
            pages = [(p.extract_text() or "") for p in pdf.pages]
            text = "\n".join(pages)
        else:
            text = ""
        if text != "":
            collection_adder(col, text, name)
            seen.add(name)



question = st.chat_input(
    "Ask something about the article",
    disabled=not uploaded_files,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the article"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if question and uploaded_files:

    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    # User asks a question: retrieve similar chunks and generate an answer 

    collection = st.session_state["collection"]
    res = collection.query(query_texts=[question], n_results=4)
    ctx = "\n\n".join(res.get("documents",[[]])[0]) if res else ""

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="openai.gpt-4o",  
            messages=[
                {"role":"system","content":"Answer ONLY from the context. If unknown, say you don't know."},
                {"role":"user","content":f"Context:\n{ctx}\n\nQuestion: {question}"},
                *st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)

    # Append the assistant's response to the messages
    st.session_state.messages.append({"role": "assistant", "content": response})