import streamlit as st
import ollama
from typing import List
import time

# Set page config for standalone window
st.set_page_config(
    page_title="NeuralNexus - Local LLM Interface",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Add custom CSS for a more compact interface
st.markdown("""
    <style>
    /* Main app */
    .stApp {
        background-color: #0a0a12;
        background-image: linear-gradient(45deg, #0a0a12 0%, #1a1a2f 100%);
    }
    
    /* Custom header - reduced padding and margin */
    .main-header {
        text-align: center;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        border-bottom: 2px solid #00ff9d40;
        position: relative;
    }
    
    .main-header h1 {
        font-family: 'Courier New', monospace;
        font-size: 2.7rem;
        font-weight: bold;
        margin: 0;
        color: #00ff9d;
        text-shadow: 0 0 10px #00ff9d80;
        letter-spacing: 2px;
    }
    
    .main-header p {
        color: #00ccff;
        margin: 0.4rem 0 0;
        font-size: 1.1rem;
        letter-spacing: 1px;
        text-shadow: 0 0 5px #00ccff80;
    }
    
    /* Chat title - reduced padding */
    .chat-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
        padding: 0.75rem;
        background: rgba(0, 255, 157, 0.05);
        border-radius: 8px;
        border: 1px solid #00ff9d40;
    }
    
    .chat-title h1 {
        margin: 0;
        font-size: 1.5rem;
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: #1a1a2f;
        border-right: 1px solid #00ff9d40;
    }
    
    /* Text input */
    .stTextInput > div > div > input {
        background-color: #2a2a4f;
        color: #e0e0ff;
        border: 1px solid #00ff9d40;
    }
    
    /* Markdown text */
    .stMarkdown {
        font-family: 'Courier New', monospace;
    }
    
    /* Headers with reduced margins */
    .stSidebar h1 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.75rem !important;
        font-size: 1.6rem !important;
    }
    
    .stSidebar h2, .stSidebar h3 {
        margin-top: 0.75rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Chat messages with reduced padding */
    .stChatMessage {
        background-color: #1a1a2f;
        border: 1px solid #00ff9d20;
        border-radius: 5px;
        padding: 8px;
        margin: 4px 0;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #2a2a4f;
        color: #00ff9d;
        border: 1px solid #00ff9d;
        border-radius: 5px;
        transition: all 0.3s ease;
        padding: 0.3rem 1rem !important;
        white-space: nowrap !important;
        display: inline-block !important;
        min-width: 120px !important;
    }
    
    .stButton > button:hover {
        background-color: #00ff9d;
        color: #0a0a12;
        box-shadow: 0 0 15px #00ff9d40;
    }
    
    /* Fix for vertical text in button */
    .clear-chat-btn span {
        display: inline-block !important;
        white-space: nowrap !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #2a2a4f;
        border: 1px solid #00ff9d40;
    }
    
    /* Smaller tab text */
    button[data-baseweb="tab"] {
        font-size: 0.85rem !important;
        padding: 0.5rem 0.75rem !important;
    }
    
    /* Expander padding */
    .streamlit-expanderHeader {
        font-size: 0.9rem;
        padding: 0.5rem;
    }
    
    /* Reduce caption size */
    .caption {
        font-size: 0.8rem !important;
    }
    
    /* Header spacing */
    h1, h2, h3 {
        color: #00ff9d !important;
        text-shadow: 0 0 10px #00ff9d40;
        margin-top: 0.75rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Help text */
    .helper-text {
        font-size: 0.8rem !important;
        padding-top: 0.25rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Add custom header
st.markdown("""
    <div class="main-header">
        <h1>NeuralNexus</h1>
        <p>Your Local AI Command Center</p>
    </div>
""", unsafe_allow_html=True)

def get_installed_models():
    try:
        response = ollama.list()
        return [model['name'] for model in response.get('models', [])]
    except Exception as e:
        st.error(f"Error fetching models: {str(e)}")
        return []

def format_size(size_bytes):
    """Convert size in bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def download_model(model_name):
    """Download a model and show progress"""
    try:
        with st.spinner(f'Downloading {model_name}... This may take a while.'):
            ollama.pull(model_name)
        st.success(f'Successfully downloaded {model_name}!')
        return True
    except Exception as e:
        st.error(f'Error downloading {model_name}: {str(e)}')
        return False

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = None
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "context_length" not in st.session_state:
    st.session_state.context_length = 4096
if "num_gpu" not in st.session_state:
    st.session_state.num_gpu = 1
if "num_thread" not in st.session_state:
    st.session_state.num_thread = 4

# Get installed models
installed_models = get_installed_models()

# Popular models list
POPULAR_MODELS = {
    "llama2": "Meta's LLaMA 2 model - Good all-rounder",
    "mistral": "Mistral 7B - Excellent performance for its size",
    "codellama": "Code-specialized LLaMA model",
    "neural-chat": "Fast and efficient chat model",
    "starling-lm": "High quality open source chat model",
    "dolphin-phi": "Lightweight yet capable model",
    "llava": "Multimodal model - can understand images",
    "deepseek": "DeepSeek Coder - Excellent for code generation and completion",
}

# Sidebar for model selection and configuration - more compact layout
with st.sidebar:
    st.title("🧠 NeuralNexus Settings")
    
    # Model management section - more compact
    st.subheader("Model Management")
    
    tab1, tab2 = st.tabs(["🔄 Select", "📥 Download"])
    
    with tab1:
        if not installed_models:
            st.warning("No models installed! Go to 'Download' tab →")
            st.info("Click the 'Download' tab above.")
            st.stop()
        
        # Model selection - always visible
        st.session_state.model = st.selectbox(
            "Select Model",
            installed_models,
            index=0 if st.session_state.model is None else installed_models.index(st.session_state.model)
        )
        
        # Basic model info - always visible
        try:
            model_info = ollama.show(st.session_state.model)
            if isinstance(model_info, dict) and 'size' in model_info:
                st.caption(f"Model size: {format_size(model_info['size'])}")
        except Exception:
            pass
    
    with tab2:
        # Popular models download - more compact
        st.markdown("#### Popular Models")
        for model_name, description in POPULAR_MODELS.items():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{model_name}**")
                st.caption(description)
            with col2:
                if model_name not in installed_models:
                    if st.button("📥", key=f"download_{model_name}", help=f"Download {model_name}"):
                        if download_model(model_name):
                            st.rerun()
                else:
                    st.markdown("✓")
        
        # Custom model download
        st.markdown("#### Custom Model")
        custom_model = st.text_input("Model name", placeholder="e.g., orca-mini")
        if custom_model:
            if st.button("Download"):
                if download_model(custom_model):
                    st.rerun()

    st.markdown("---")
    
    # Advanced settings in an expander
    with st.expander("⚙️ Advanced Settings"):
        st.markdown("#### Model Configuration")
        
        # Generation settings
        st.markdown("##### Generation")
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            help="Higher = more random, lower = more deterministic"
        )
        
        st.session_state.context_length = st.slider(
            "Context Length",
            min_value=512,
            max_value=8192,
            value=4096,
            step=512,
            help="Number of tokens to consider for context"
        )
        
        # Hardware settings
        st.markdown("##### Hardware")
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.num_gpu = st.number_input(
                "GPUs",
                min_value=0,
                max_value=8,
                value=1,
                help="Number of GPUs to use (0 for CPU only)"
            )
        
        with col2:
            st.session_state.num_thread = st.number_input(
                "Threads",
                min_value=1,
                max_value=16,
                value=4,
                help="Number of CPU threads to use"
            )
        
        # Detailed model information - more compact
        if isinstance(model_info, dict):
            st.markdown("##### Model Info")
            st.markdown(f"**Name:** {st.session_state.model}")
            if 'modified_at' in model_info:
                st.markdown(f"**Modified:** {model_info['modified_at']}")
            if 'details' in model_info:
                details = model_info['details']
                st.markdown(f"**Format:** {details.get('format', 'N/A')}")
    
    # More compact about section
    st.markdown("---")
    st.caption("""
    **About:** A simple interface for Ollama models.
    Select a model and start chatting!
    """)

# Main chat interface - more compact
st.markdown("""
    <div class="chat-title">
        <h1>💬 Neural Interface</h1>
    </div>
""", unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Stream the response with configuration
            stream = ollama.chat(
                model=st.session_state.model,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
                options={
                    "temperature": st.session_state.temperature,
                    "num_ctx": st.session_state.context_length,
                    "num_gpu": st.session_state.num_gpu,
                    "num_thread": st.session_state.num_thread
                }
            )
            
            for chunk in stream:
                if chunk.get('message', {}).get('content'):
                    full_response += chunk['message']['content']
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.01)
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            full_response = "Sorry, I encountered an error. Please try again."
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Fixed clear chat button with custom formatting
st.markdown('<div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">', unsafe_allow_html=True)
if st.button("🗑️ Clear", key="clear_chat"):
    st.session_state.messages = []
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True) 