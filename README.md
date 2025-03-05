# NeuralNexus

![NeuralNexus](https://img.shields.io/badge/NeuralNexus-Local_LLM_Interface-00ff9d)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B)
![Ollama](https://img.shields.io/badge/Ollama-0.1.6-gray)

A sleek, cyberpunk-themed interface for running and interacting with Large Language Models locally through Ollama.

## 🧠 Features

- **Local LLM Management**: Download, manage, and run various LLM models locally
- **Seamless Chat Interface**: Interact with your local models through a modern chat UI
- **Smart Memory Management**: Auto-unload models when not in use to save system resources
- **Real-time Status Updates**: See the actual load status of your models with accurate indicators
- **Preload Capability**: Load models before chatting with a single click
- **Advanced Model Configuration**: Control temperature, context length, GPU, and CPU thread settings
- **Cyberpunk UI**: Enjoy a visually appealing dark-themed interface with neon accents

## 📋 Requirements

- Python 3.8+
- Ollama installed locally ([Get Ollama](https://ollama.ai/))

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/neuralnexus.git
cd neuralnexus
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application with the desktop window:
```bash
python3 window.py
```

Or run as a web app:
```bash
streamlit run app.py
```

## 💻 Usage

1. Select or download a model from the sidebar
2. Configure your model settings (optional)
3. Start chatting with your local AI!

## 🔧 Advanced Settings

- **Temperature**: Control the randomness of generated responses
- **Context Length**: Adjust the token context window size
- **GPU Settings**: Set the number of GPUs to use
- **CPU Threads**: Control the number of CPU threads
- **Auto-unload**: Toggle automatic unloading of models when the app is inactive to save memory

## 📝 License

MIT License

## 🙏 Acknowledgements

- [Ollama](https://ollama.ai/) for making local LLMs accessible
- [Streamlit](https://streamlit.io/) for the web app framework
- [PyWebView](https://pywebview.flowrl.com/) for the native desktop interface 