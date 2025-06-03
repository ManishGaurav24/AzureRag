import os
import base64
import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
#Manish1st
# Azure OpenAI configuration
endpoint = os.getenv("ENDPOINT_URL", "https://hubproject00200356835591.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://testaisearch006.search.windows.net/")
search_key = os.getenv("SEARCH_KEY", "put your Azure AI Search admin key here")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")

def call_llm(user_input):
    # Initialize Azure OpenAI Service client with key-based authentication
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version="2025-01-01-preview",
    )

    # Prepare the chat prompt
    prompt_content = "You are an AI assistant that helps me with queries in my document"
    chat_prompt = [
        {
            "role": "system",
            "content": f"{prompt_content}"
        },
        {
            "role": "user",
            "content": f"{user_input}"
        }
    ]
    
    # Include speech result if speech is enabled
    messages = chat_prompt
    
    # Generate the completion
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False,
        extra_body={
            "data_sources": [{
                "type": "azure_search",
                "parameters": {
                    "filter": None,
                    "endpoint": f"{search_endpoint}",
                    "index_name": "azureblob-indexv1",
                    "semantic_configuration": "testsemantic",
                    "authentication": {
                        "type": "api_key",
                        "key": f"{search_key}"
                    },
                    "embedding_dependency": {
                        "type": "endpoint",
                        "endpoint": "https://hubproject00200356835591.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15",
                        "authentication": {
                            "type": "api_key",
                            "key": "2E7P8hbwiEQ7euSTx8VTgl00dlAmg0z4XXbdREq7jTXfzoCTcgt0JQQJ99BFACfhMk5XJ3w3AAAAACOGGjiU"
                        }
                    },
                    "query_type": "semantic",
                    "in_scope": True,
                    # Removed the problematic "role_information" parameter
                    "strictness": 3,
                    "top_n_documents": 5
                }
            }]
        }
    )
    
    return completion.choices[0].message.content

# Set up Streamlit UI
st.set_page_config(page_title="Document Assistant Chatbot", page_icon="📚")

st.title("Document Assistant Chatbot")
st.subheader("Ask questions about your documents")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = call_llm(prompt)
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_message = f"Error: {str(e)}"
                st.error(error_message)
                # Add error message to chat history
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# Add some instructions
with st.sidebar:
    st.markdown("### Instructions")
    st.markdown("""
    1. Enter your question in the chat input
    2. The AI will search through your documents and provide an answer
    3. Your conversation history will be maintained during this session
    """)
    
    st.markdown("### Environment Setup")
    st.markdown("""
    Make sure you have set the following environment variables:
    - ENDPOINT_URL
    - DEPLOYMENT_NAME
    - SEARCH_ENDPOINT
    - SEARCH_KEY
    - AZURE_OPENAI_API_KEY
    """)
    
    # Optional section for setting credentials via UI
    with st.expander("Update API Credentials"):
        endpoint_input = st.text_input("Azure OpenAI Endpoint", endpoint)
        deployment_input = st.text_input("Deployment Name", deployment)
        api_key_input = st.text_input("Azure OpenAI API Key", subscription_key, type="password")
        search_endpoint_input = st.text_input("Search Endpoint", search_endpoint)
        search_key_input = st.text_input("Search Key", search_key, type="password")
        
        if st.button("Update Credentials"):
            endpoint = endpoint_input
            deployment = deployment_input
            subscription_key = api_key_input
            search_endpoint = search_endpoint_input
            search_key = search_key_input
            st.success("Credentials updated!")