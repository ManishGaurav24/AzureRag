import os
import base64
import json
import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI configuration
endpoint = os.getenv("ENDPOINT_URL", "https://ai22042580088494.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://sampledocservice.search.windows.net/")
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
                    "index_name": "frosty-guava-ffffs91xq0",
                    "semantic_configuration": "azureml-default",
                    "authentication": {
                        "type": "api_key",
                        "key": f"{search_key}"
                    },
                    "embedding_dependency": {
                        "type": "endpoint",
                        "endpoint": "https://ai22042580088494.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-07-01-preview",
                        "authentication": {
                            "type": "api_key",
                            "key": "CmYU1rinyJ9cZtPt50KacbJPdCCgJV0g8taqRZEEIkIjNM326wn7JQQJ99BDACHYHv6XJ3w3AAAAACOGLmr2"
                        }
                    },
                    "query_type": "vector_simple_hybrid",
                    "in_scope": True,
                    "strictness": 3,
                    "top_n_documents": 5
                }
            }]
        }
    )
    
    # Get the full JSON response for debugging
    raw_response = json.loads(completion.model_dump_json())
    
    return completion.choices[0].message.content, raw_response

# Set up Streamlit UI
st.set_page_config(page_title="Document Assistant Chatbot", page_icon="📚", layout="wide")

st.title("Document Assistant Chatbot")
st.subheader("Ask questions about your documents")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create a two-column layout
col1, col2 = st.columns([2, 1])

with col1:
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
                    response, raw_response = call_llm(prompt)
                    st.markdown(response)
                    
                    # Store the raw response for debugging
                    if "raw_responses" not in st.session_state:
                        st.session_state.raw_responses = []
                    st.session_state.raw_responses.append(raw_response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "raw_response": raw_response
                    })
                except Exception as e:
                    error_message = f"Error: {str(e)}"
                    st.error(error_message)
                    # Add error message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

with col2:
    st.markdown("### Response Debug Panel")
    
    if "raw_responses" in st.session_state and st.session_state.raw_responses:
        latest_response = st.session_state.raw_responses[-1]
        
        # Try to extract context and tool messages
        st.markdown("#### Response Structure")
        if "context" in latest_response and "messages" in latest_response["context"]:
            st.success("Context and messages found!")
            for i, message in enumerate(latest_response["context"]["messages"]):
                st.markdown(f"**Message {i+1} (Role: {message.get('role', 'unknown')}):**")
                with st.expander(f"View Message {i+1} Content"):
                    st.json(message)
        else:
            st.warning("Context or messages not found in the response")
        
        # Look for citations or contexts
        contexts_found = False
        if "choices" in latest_response and latest_response["choices"]:
            choice = latest_response["choices"][0]
            if "message" in choice:
                message = choice["message"]
                if "context" in message:
                    contexts_found = True
                    st.success("Context found in message!")
                    with st.expander("View Message Context"):
                        st.json(message["context"])
                if "tool_calls" in message:
                    contexts_found = True
                    st.success("Tool calls found in message!")
                    with st.expander("View Tool Calls"):
                        st.json(message["tool_calls"])
        
        if not contexts_found:
            st.warning("No citations or contexts found in the message")
        
        # Show the full raw response
        with st.expander("View Full Raw Response"):
            st.json(latest_response)
        
        # Manual extraction of potential chunks
        st.markdown("#### Document Chunks Extraction")
        
        def extract_chunks(obj, prefix=""):
            chunks = []
            if isinstance(obj, dict):
                # Look for fields that might contain chunks
                for key in ["citations", "documents", "content", "chunks", "results", "contexts"]:
                    if key in obj:
                        st.success(f"Found potential chunks under '{prefix}{key}'")
                        with st.expander(f"View '{key}' content"):
                            st.json(obj[key])
                
                # Recursively search all dictionary fields
                for key, value in obj.items():
                    sub_chunks = extract_chunks(value, f"{prefix}{key}.")
                    chunks.extend(sub_chunks)
            elif isinstance(obj, list):
                # Recursively search all list items
                for i, item in enumerate(obj):
                    sub_chunks = extract_chunks(item, f"{prefix}[{i}].")
                    chunks.extend(sub_chunks)
            return chunks
        
        extract_chunks(latest_response)

# Add instructions to the sidebar
with st.sidebar:
    st.markdown("### Instructions")
    st.markdown("""
    1. Enter your question in the chat input
    2. The AI will search through your documents and provide an answer
    3. View the debug panel to explore the raw response
    4. Your conversation history will be maintained during this session
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