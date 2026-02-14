# 🏦 HBDB Banking Bot - Streamlit Application

A comprehensive banking chatbot powered by **Mistral AI's large language model** that provides instant support for HBDB (Hadean Bank Database) customers.

## 🚀 Features

- **AI-Powered Chat**: Uses Mistral-large-latest model for intelligent responses
- **FAQ Database Integration**: Automatically references 45+ banking FAQs
- **Real-time Responses**: Instant answers to banking queries
- **Conversation Memory**: Maintains chat history for context-aware responses
- **Professional UI**: Clean, intuitive Streamlit interface
- **Secure API Integration**: Supports secure API key management

## 📋 Prerequisites

- Python 3.8+
- Virtual environment (recommended)
- Mistral AI API Key (get it from [Mistral Console](https://console.mistral.ai))

## 📦 Installation

### 1. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install streamlit mistralai pandas
```

## 🔑 API Key Setup

You need a Mistral AI API key to run the bot:

1. Visit [Mistral Console](https://console.mistral.ai)
2. Sign up or log in to your account
3. Generate an API key
4. Save it securely

## ▶️ Running the Application

```bash
streamlit run banking_bot.py
```

The application will automatically open in your browser at:
- **Local**: http://localhost:8502
- **Network**: http://192.168.1.229:8502 (or your machine's IP)

## 🎯 Usage

1. **Enter API Key**: Paste your Mistral AI API key in the sidebar
2. **Ask Questions**: Type your banking questions in the chat input
3. **Get Answers**: The bot will respond using the FAQ database and AI model
4. **Continue Conversation**: Chat history is maintained for context

## 📊 Banking Services Covered

The bot provides support for:
- Account opening and management
- Online & mobile banking
- Credit and debit cards
- Loans (personal, auto, mortgage)
- Wire transfers and global services
- Bill payments and overdraft protection
- Account security and fraud reporting
- And much more!

## 📁 Project Structure

```
Banking 14 fab/
├── banking_bot.py                    # Main Streamlit application
├── hbdb_banking_faqs (2) (1).csv    # FAQ database
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## 🔧 Configuration

### Environment Variables (Optional)
You can set your API key as an environment variable to skip entering it each time:

```bash
export MISTRAL_API_KEY="your-api-key-here"
```

## 📝 Requirements.txt

```
streamlit==1.54.0
mistralai==1.12.2
pandas==2.3.3
```

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'mistralai'"
**Solution**: Make sure you're in the virtual environment and have installed all dependencies:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Invalid API Key"
**Solution**: Verify your Mistral AI API key is correct and has proper permissions

### Issue: Port 8502 already in use
**Solution**: Use a different port:
```bash
streamlit run banking_bot.py --server.port 8503
```

## 🌐 Accessing Remotely

To access the app from another machine on your network:
- Use the Network URL provided by Streamlit (e.g., http://192.168.1.229:8502)
- Or configure port forwarding if accessing from outside your network

## 📚 FAQ Database

The bot references a CSV file containing 45+ banking FAQs covering:
- Account types and opening procedures
- Online and mobile banking features
- Credit and lending products
- Transaction services
- Account security and support

## 🤝 Support

For issues or questions:
1. Check Streamlit documentation: https://docs.streamlit.io
2. Check Mistral AI documentation: https://docs.mistral.ai
3. Review the FAQ database for common banking questions

## ⚡ Performance Tips

1. Install Watchdog for better file watching:
   ```bash
   pip install watchdog
   ```

2. Use the network URL for faster local network access

3. Keep your FAQ database updated with current banking information

## 🔐 Security Notes

- **Never hardcode API keys** in the source code
- **Use environment variables** or secure key management
- **API keys in the sidebar** are password-masked
- **Keep your API key confidential**

## 📄 License

This project is provided as-is for demonstration purposes.

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Mistral AI API Guide](https://docs.mistral.ai)
- [Python Virtual Environments](https://docs.python.org/3/library/venv.html)

---

**Version**: 1.0.0  
**Last Updated**: February 14, 2026  
**Built with**: Streamlit + Mistral AI
