import streamlit as st
import ollama
from typing import List
import time
import requests
import streamlit.components.v1 as components

# Set page config for standalone window
st.set_page_config(
    page_title="NeuralNexus - Local LLM Interface",
    page_icon="⚡",
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
    /* Main app with circuit pattern background */
    .stApp {
        background-color: #0a0a12;
        background-image: 
            linear-gradient(45deg, #0a0a12 0%, #1a1a2f 100%),
            linear-gradient(90deg, rgba(0, 255, 157, 0.05) 1px, transparent 1px),
            linear-gradient(0deg, rgba(0, 255, 157, 0.05) 1px, transparent 1px);
        background-size: 100% 100%, 20px 20px, 20px 20px;
        background-position: 0 0, 0 0, 0 0;
    }
    
    /* Custom header with enhanced glow */
    .main-header {
        text-align: center;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        border-bottom: 2px solid #00ff9d40;
        position: relative;
        background: rgba(10, 10, 18, 0.7);
        backdrop-filter: blur(5px);
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 255, 157, 0.1);
    }
    
    .main-header h1 {
        font-family: 'Courier New', monospace;
        font-size: 2.7rem;
        font-weight: bold;
        margin: 0;
        color: #00ff9d;
        text-shadow: 0 0 10px #00ff9d80, 0 0 20px #00ff9d40;
        letter-spacing: 2px;
    }
    
    .main-header p {
        color: #00ccff;
        margin: 0.4rem 0 0;
        font-size: 1.1rem;
        letter-spacing: 1px;
        text-shadow: 0 0 5px #00ccff80, 0 0 10px #00ccff40;
    }
    
    /* Chat title with enhanced tech look */
    .chat-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
        padding: 0.75rem;
        background: rgba(0, 255, 157, 0.05);
        border-radius: 8px;
        border: 1px solid #00ff9d40;
        box-shadow: inset 0 0 8px rgba(0, 255, 157, 0.2);
        backdrop-filter: blur(2px);
    }
    
    .chat-title h1 {
        margin: 0;
        font-size: 1.5rem;
    }
    
    /* Sidebar with circuit edge detail */
    .stSidebar {
        background-color: #1a1a2f;
        border-right: 1px solid #00ff9d40;
        box-shadow: inset -5px 0 15px rgba(0, 0, 0, 0.3);
        background-image: 
            linear-gradient(90deg, rgba(0, 255, 157, 0.03) 1px, transparent 1px),
            linear-gradient(0deg, rgba(0, 255, 157, 0.03) 1px, transparent 1px);
        background-size: 15px 15px;
    }
    
    /* Text input with glow effect */
    .stTextInput > div > div > input {
        background-color: #2a2a4f;
        color: #e0e0ff;
        border: 1px solid #00ff9d40;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border: 1px solid #00ff9d;
        box-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
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
    
    /* Chat messages with enhanced styling */
    .stChatMessage {
        background-color: #1a1a2f;
        border: 1px solid #00ff9d20;
        border-radius: 5px;
        padding: 8px;
        margin: 4px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    /* Buttons with circuit-inspired hover effect */
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
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        background-color: #00ff9d20;
        color: #00ff9d;
        box-shadow: 0 0 15px rgba(0, 255, 157, 0.5);
        border-color: #00ffbd;
    }
    
    .stButton > button:hover:after {
        content: '';
        position: absolute;
        top: 0;
        left: -50%;
        width: 150%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 157, 0.2), transparent);
        transform: skewX(-20deg);
        animation: circuit-flow 1s linear;
    }
    
    @keyframes circuit-flow {
        0% { left: -50%; }
        100% { left: 100%; }
    }
    
    /* Fix for vertical text in button */
    .clear-chat-btn span {
        display: inline-block !important;
        white-space: nowrap !important;
    }
    
    /* Selectbox with tech styling */
    .stSelectbox > div > div {
        background-color: #2a2a4f;
        border: 1px solid #00ff9d40;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #00ff9d;
        box-shadow: 0 0 8px rgba(0, 255, 157, 0.3);
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

# Add JavaScript for visibility detection to handle auto-unload
if 'auto_unload' in st.session_state and st.session_state.auto_unload:
    # Custom handler for visibility change
    st.markdown("""
    <script>
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'hidden') {
            // When tab is hidden, trigger auto-unload
            const data = new FormData();
            data.append('data', 'unload_model');
            // Use the streamlit's own fetch API to communicate with the server
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'unload_model'}, '*');
        }
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Handle the visibility change with a custom component
    def visibility_handler():
        trigger = components.html(
            """
            <div id="visibility-trigger" style="display:none;"></div>
            <script>
            // This will be called when the component is created or updated
            function sendMessageToStreamlit(e) {
                if (e.data.type === 'streamlit:componentReady') {
                    // Send any initial data
                }
            }
            // Listen for messages from the parent frame
            window.addEventListener('message', sendMessageToStreamlit);
            </script>
            """,
            height=0,
            key="visibility_handler"
        )
        
        # Check if the model needs to be unloaded
        if trigger == 'unload_model' and st.session_state.model:
            # Only try to unload if auto_unload is enabled
            if not st.session_state.get('auto_unload', False):
                return
                
            # Only try to unload if we think it might be loaded
            if check_model_loaded(st.session_state.model):
                # Try to unload
                unload_model(st.session_state.model)
            else:
                # Just update our state
                st.session_state.model_loaded = False
            # We don't rerun here because it would interrupt user's flow
    
    # Call the handler
    visibility_handler()

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

def check_model_loaded(model_name):
    """Check if a model is actually loaded in memory by making a simple API call"""
    if not model_name:
        return False
    
    try:
        # Use list running models to check if model is loaded
        response = requests.get(
            'http://localhost:11434/api/ps',
            timeout=2.0  # Reasonable timeout
        )
        
        if response.status_code != 200:
            return False
            
        # Check if our model is in the list of running models 
        data = response.json()
        models = data.get('models', [])
        
        # Look for our model in the currently running models
        for model in models:
            if model.get('model') == model_name:
                return True
                
        return False
    except Exception as e:
        # Log the error for debugging but don't show in console
        # print(f"Error checking model loaded status: {str(e)}")
        # For any exception, assume model is not loaded
        return False

def unload_model(model_name):
    """Unload a model from memory"""
    try:
        if model_name:
            # First check if the model is actually loaded
            if not check_model_loaded(model_name):
                st.success(f"Model {model_name} is already unloaded")
                st.session_state.model_loaded = False
                return True
            
            # Use the keep_alive=0 parameter to unload the model
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={"model": model_name, "keep_alive": 0, "prompt": ""}
            )
            
            # Wait a moment for unload to take effect
            time.sleep(1)
            
            # Check if the model was actually unloaded
            still_loaded = check_model_loaded(model_name)
            
            if not still_loaded:
                st.success(f"Successfully unloaded {model_name} from memory")
                # Directly update the session state
                st.session_state.model_loaded = False
                return True
            else:
                st.warning(f"Attempted to unload {model_name}, but it's still in memory")
                st.session_state.model_loaded = True
                return False
    except Exception as e:
        st.error(f"Error unloading model: {str(e)}")
        return False

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
if "auto_unload" not in st.session_state:
    st.session_state.auto_unload = False
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = True
if "visibility_state" not in st.session_state:
    st.session_state.visibility_state = "visible"
if "just_loaded_model" not in st.session_state:
    st.session_state.just_loaded_model = False

# Callback for auto-unload toggle
def on_auto_unload_change():
    if st.session_state.auto_unload_toggle:
        st.session_state.auto_unload = True
    else:
        st.session_state.auto_unload = False

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
    st.title("⚡ NeuralNexus Settings")
    
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
            
            # Only check actual loaded status if we have a stable connection
            try:
                # Check actual model status and update session state
                actual_loaded_state = check_model_loaded(st.session_state.model)
                
                # If our state doesn't match reality, update it silently
                if actual_loaded_state != st.session_state.get('model_loaded', False):
                    st.session_state.model_loaded = actual_loaded_state
                
                # Show load status with clear visual indicators
                if actual_loaded_state:
                    st.markdown("📊 Status: <span style='color:#00ff9d;font-weight:bold;'>Loaded in memory</span>", unsafe_allow_html=True)
                else:
                    st.markdown("💤 Status: <span style='color:#ff9d9d;font-weight:bold;'>Unloaded from memory</span>", unsafe_allow_html=True)
            except Exception:
                # If we can't check the status, show unknown
                st.markdown("❓ Status: <span style='color:#ffcc00;font-weight:bold;'>Unknown</span>", unsafe_allow_html=True)
                
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
        
        # Memory management section
        st.markdown("##### Memory Management")
        
        # Unload button
        # First check actual model status
        actual_loaded_state = check_model_loaded(st.session_state.model)
        
        # Always show the button, but change its appearance based on load state
        if actual_loaded_state:
            # Model is loaded - show unload button
            if st.button("⚡ Unload Model", 
                         help="Unload the model from memory to free up resources",
                         type="primary"):
                if unload_model(st.session_state.model):
                    st.rerun()
        else:
            # Model is already unloaded - show disabled-style button
            st.button("✓ Model Unloaded", 
                    help="This model is already unloaded from memory",
                    disabled=True)
        
        # Auto-unload toggle
        st.toggle(
            "Auto-unload when inactive", 
            value=st.session_state.get('auto_unload', False),
            key="auto_unload_toggle",
            on_change=on_auto_unload_change,
            help="Automatically unload the model when you navigate away and reload when you chat"
        )
        
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
    **About:** Advanced neural interface for Ollama models.
    Select a model and initiate neural connection.
    """)

# Main chat interface - more compact
st.markdown("""
    <div class="chat-title">
        <h1>🔮 Neural Interface</h1>
    </div>
""", unsafe_allow_html=True)

# Check if we need to refresh the status (model was just loaded in previous interaction)
if st.session_state.get('just_loaded_model', False):
    # Clear the flag
    st.session_state.just_loaded_model = False
    # Give the UI a moment to update first
    st.rerun()

# Add status indicator in the main chat area that updates with each interaction
if st.session_state.model:
    status_col1, status_col2 = st.columns([1, 4])
    with status_col1:
        loaded = check_model_loaded(st.session_state.model)
        if loaded:
            st.markdown("📊 <span style='color:#00ff9d;font-weight:bold;'>Model Status: Loaded</span>", unsafe_allow_html=True)
        else:
            st.markdown("💤 <span style='color:#ff9d9d;font-weight:bold;'>Model Status: Unloaded</span>", unsafe_allow_html=True)
    with status_col2:
        if not loaded and st.button("⚡ Load Model Now", help="Preload the model without waiting for chat"):
            # Try to load the model with a simple request
            try:
                requests.post(
                    'http://localhost:11434/api/generate',
                    json={"model": st.session_state.model, "prompt": " ", "stream": False},
                    timeout=1
                )
                st.session_state.model_loaded = True
                st.experimental_rerun()
            except:
                st.error("Failed to load model. Try chatting to automatically load it.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history first
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Check if model is available
            model_loaded = check_model_loaded(st.session_state.model)
            if not model_loaded:
                # Show loading message
                message_placeholder.info(f"Model {st.session_state.model} is being loaded...")
            
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
            
            # If we get here, the model is loaded
            st.session_state.model_loaded = True
            
            # Set a flag to indicate we've just loaded the model
            if not model_loaded:
                st.session_state.just_loaded_model = True
            
            for chunk in stream:
                if chunk.get('message', {}).get('content'):
                    full_response += chunk['message']['content']
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.01)
            
            message_placeholder.markdown(full_response)
            
            # After a successful response, ensure model status is up to date
            if not model_loaded:
                # We loaded the model during this interaction
                st.session_state.just_loaded_model = True
                
                # Add assistant response to chat history before rerunning
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                # Force an immediate rerun to update all status indicators
                st.rerun()
            
        except Exception as e:
            error_msg = str(e)
            st.error(f"Error: {error_msg}")
            
            # Check if this is a model loading error and update state
            if "failed to load model" in error_msg.lower():
                st.session_state.model_loaded = False
                st.info("Please try again - model will be reloaded")
                
            full_response = "Sorry, I encountered an error. Please try again."
        
        # Add assistant response to chat history (only if we didn't already do it above)
        if not st.session_state.get('just_loaded_model', False):
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Fixed clear chat button with custom formatting
st.markdown('<div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">', unsafe_allow_html=True)
if st.button("🗑️ Clear", key="clear_chat"):
    st.session_state.messages = []
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True) 