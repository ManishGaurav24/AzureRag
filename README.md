# Document Assistant Chatbot

A powerful chatbot built with Azure OpenAI, Azure AI Search, and Streamlit that helps users interact with their documents using natural language.

<div align="center">
  <img src="https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/azure.png" width="100">
  <img src="https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg" width="100">
  <img src="https://www.pinecone.io/images/illustrations/rag.png" width="100">
</div>

## 🚀 Project Overview

This project implements a document chatbot that leverages Azure OpenAI's GPT models and Azure AI Search for efficient document retrieval and question answering. The application uses RAG (Retrieval-Augmented Generation) architecture to provide accurate responses based on the content of your documents.

## 📁 Project Structure

```
AzurePlayground/
├── app.py              # Main Streamlit application
├── appChunk.py         # Enhanced version with chunk debugging
├── playground.py       # Development playground
├── playground2.py      # Alternative implementation
├── chunk.txt          # Sample chunk data
├── .env               # Environment variables (not tracked in git)
└── README.md          # Project documentation
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AzurePlayground
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. Install required packages:
```bash
pip install streamlit openai python-dotenv azure-identity
```

4. Create a `.env` file with your Azure credentials:
```bash
ENDPOINT_URL="your-azure-openai-endpoint"
DEPLOYMENT_NAME="your-deployment-name"
SEARCH_ENDPOINT="your-azure-search-endpoint"
SEARCH_KEY="your-search-admin-key"
AZURE_OPENAI_API_KEY="your-azure-openai-key"
```

## 🚀 Running the Application

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

## 🔧 Features

- 💬 Interactive chat interface
- 🔍 Document search using Azure AI Search
- 🧠 Azure OpenAI GPT model integration
- 📊 Debug panel for response analysis (in appChunk.py)
- 🔐 Secure credential management
- 💾 Session state management for chat history

## 🔑 Configuration

The application can be configured through:
- Environment variables in `.env` file
- UI-based credential updates in the sidebar
- Application settings in the code

## 🏗️ Architecture

This project uses a RAG (Retrieval-Augmented Generation) architecture:
1. User queries are processed by Azure OpenAI
2. Relevant documents are retrieved from Azure AI Search
3. Context is combined with the query for accurate responses
4. Results are presented through a Streamlit interface

## ⚙️ Environment Variables

Required environment variables:
- `ENDPOINT_URL`: Azure OpenAI endpoint
- `DEPLOYMENT_NAME`: Model deployment name
- `SEARCH_ENDPOINT`: Azure AI Search endpoint
- `SEARCH_KEY`: Search service admin key
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key

## 📝 License

[Add your license information here]

## 👥 Contributors

[Add contributor information here]
