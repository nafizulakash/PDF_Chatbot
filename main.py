import streamlit as st
from pdf_reader import extract_text_from_pdf
from llm_client import NemotronClient

# Page config
st.set_page_config(
    page_title="PDF ChatBot",
    page_icon="📄",
    layout="wide"
)

# Black theme CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        [data-testid="stSidebar"] {
            background-color: #2d2d2d;
        }
        .user-msg {
            background-color: #0084ff;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            color: white;
            text-align: right;
        }
        .bot-msg {
            background-color: #404040;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            color: #e0e0e0;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📄 PDF ChatBot")

# Initialize session state
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "llm_client" not in st.session_state:
    st.session_state.llm_client = NemotronClient()

# Sidebar
with st.sidebar:
    st.header("📤 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner("Reading PDF..."):
            st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("✅ PDF loaded!")
        
        if st.button("Clear PDF"):
            st.session_state.pdf_text = None
            st.session_state.chat_history = []
            st.rerun()

# Main area
if st.session_state.pdf_text is None:
    st.info("👆 Upload a PDF from the sidebar to start")
else:
    st.success("✅ PDF loaded! Ask your questions below.")
    
    # Display chat
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # Input
    st.divider()
    user_input = st.text_input("Ask a question:", placeholder="What does this PDF say about...?")
    
    if user_input:
        # Create message for API
        system_message = f"You are a helpful assistant. Answer questions based ONLY on this PDF content:\n\n{st.session_state.pdf_text[:3000]}"
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ]
        
        # Get response
        with st.spinner("Thinking..."):
            response = st.session_state.llm_client.chat(messages)
        
        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "bot", "content": response})
        
        st.rerun()