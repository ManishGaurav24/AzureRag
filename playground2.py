# import os  
# import base64
# from openai import AzureOpenAI  

# endpoint = os.getenv("ENDPOINT_URL", "https://ai22042580088494.openai.azure.com/")  
# deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")  
# search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://sampledocservice.search.windows.net/")  
# search_key = os.getenv("SEARCH_KEY", "put your Azure AI Search admin key here")  
# subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")  

# def call_llm(user_input):
# # Initialize Azure OpenAI Service client with key-based authentication    
# client = AzureOpenAI(  
#     azure_endpoint=endpoint,  
#     api_key=subscription_key,  
#     api_version="2025-01-01-preview",
# )

# #Prepare the chat prompt 
# prompt_content = "You are an AI assistant that helps me with queries in my document"
# chat_prompt = [
#         {
#             "role": "system",
#             "content": f"{prompt_content}"
#         },
#         {
#             "role": "user",
#             "content": f"{user_input}"
#         }
#     ]
    
# # Include speech result if speech is enabled  
# messages = chat_prompt  
    
# # Generate the completion  
# completion = client.chat.completions.create(  
#     model=deployment,
#     messages=messages,
#     max_tokens=800,  
#     temperature=0.7,  
#     top_p=0.95,  
#     frequency_penalty=0,  
#     presence_penalty=0,
#     stop=None,  
#     stream=False,
#     extra_body={
#       "data_sources": [{
#           "type": "azure_search",
#           "parameters": {
#             "filter": None,
#             "endpoint": f"{search_endpoint}",
#             "index_name": "frosty-guava-ffffs91xq0",
#             "semantic_configuration": "azureml-default",
#             "authentication": {
#               "type": "api_key",
#               "key": f"{search_key}"
#             },
#             "embedding_dependency": {
#               "type": "endpoint",
#               "endpoint": "https://ai22042580088494.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-07-01-preview",
#               "authentication": {
#                 "type": "api_key",
#                 "key": "CmYU1rinyJ9cZtPt50KacbJPdCCgJV0g8taqRZEEIkIjNM326wn7JQQJ99BDACHYHv6XJ3w3AAAAACOGLmr2"
#               }
#             },
#             "query_type": "vector_simple_hybrid",
#             "in_scope": True,
#             "role_information": "You are an AI assistant that helps me with queries in my document",
#             "strictness": 3,
#             "top_n_documents": 5
#           }
#         }]
#     }
# )

# print(completion.to_json())  