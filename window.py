import webview
import subprocess
import time
import sys
import os

def run_streamlit():
    # Start Streamlit in the background with cyberpunk dark theme
    streamlit_process = subprocess.Popen(
        ['streamlit', 'run', 'app.py', 
         '--server.port', '8501', 
         '--browser.serverAddress', 'localhost',
         '--browser.serverPort', '8501',
         '--browser.gatherUsageStats', 'false',
         '--server.headless', 'true',
         '--theme.base', 'dark',
         '--theme.primaryColor', '#00ff9d',  # Neon green
         '--theme.backgroundColor', '#0a0a12',  # Deep dark blue-black
         '--theme.secondaryBackgroundColor', '#1a1a2f',  # Dark blue
         '--theme.textColor', '#e0e0ff',  # Soft blue-white
         '--theme.font', 'monospace'],  # Cyberpunk-style font
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for Streamlit to start
    time.sleep(2)
    
    # Create window with dark theme and slightly more compact size
    window = webview.create_window(
        'NeuralNexus - Local LLM Interface',
        'http://localhost:8501',
        width=1100,  # Slightly smaller width
        height=750,  # Slightly smaller height
        resizable=True,
        min_size=(800, 600),  # Reasonable minimum size
        background_color='#0a0a12'  # Match the dark background
    )
    
    # Start the window
    webview.start(debug=False)
    
    # Cleanup
    streamlit_process.terminate()

if __name__ == '__main__':
    run_streamlit() 