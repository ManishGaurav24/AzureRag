# import os
# from openai import AzureOpenAI  
# from azure.identity import DefaultAzureCredential, get_bearer_token_provider  
  
# endpoint = os.getenv("ENDPOINT_URL", "https://ai22042580088494.openai.azure.com/")
# deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
  
# # Initialize Azure OpenAI client with Entra ID authentication  
# cognitiveServicesResource = os.getenv('AZURE_COGNITIVE_SERVICES_RESOURCE', 'YOUR_COGNITIVE_SERVICES_RESOURCE')  
# token_provider = get_bearer_token_provider(  
#     DefaultAzureCredential(),  
#     f'{cognitiveServicesResource}.default'  
# )  
        
# client = AzureOpenAI(  
#     azure_endpoint=endpoint,  
#     azure_ad_token_provider=token_provider,  
#     api_version='2024-05-01-preview',  
# )  
       
# completion = client.chat.completions.create(  
#     model=deployment,  
#     messages=[
#     {
#         "role": "system",
#         "content": "You are an AI assistant that helps me with queries in my document"
#     },
#     {
#         "role": "user",
#         "content": "How many columns does the header file contain"
#     },
#     {
#         "role": "assistant",
#         "content": "The header file contains 123 columns [doc1]."
#     },
#     {
#         "role": "user",
#         "content": "SV2 bill types contain institutional (hospital, medical facility) services billed on which form"
#     },
#     {
#         "role": "assistant",
#         "content": "SV2 bill types contain institutional (hospital, medical facility) services billed on a CMS-1450 form (UB-92, UB-04) [doc1]."
#     },
#     {
#         "role": "user",
#         "content": "How many columns does the detail file contain"
#     },
#     {
#         "role": "assistant",
#         "content": "The detail file contains 51 columns [doc1]."
#     },
#     {
#         "role": "user",
#         "content": "How many columns does the header file contain"
#     },
#     {
#         "role": "assistant",
#         "content": "The header file contains 123 columns [doc1]."
#     }
# ],  
#     past_messages=10,
#     max_tokens=800,  
#     temperature=0.7,  
#     top_p=0.95,  
#     frequency_penalty=0,  
#     presence_penalty=0,  
#     stop=None,  
#     extra_body={  
#         "data_sources": [  
#             {  
#                 "type": "azure_search",  
#                 "parameters": {  
#                     "endpoint": os.environ["AZURE_AI_SEARCH_ENDPOINT"],  
#                     "index_name": os.environ["AZURE_AI_SEARCH_INDEX"],  
#                     "authentication": {  
#                         "type": "system_assigned_managed_identity"  
#                     }  
#                 }  
#             }  
#         ]  
#     }  
# )

# print(completion.model_dump_json(indent=2))  