import os
import requests
from typing import List
from promptflow.core import tool
from promptflow.contracts.multimedia import Image as PFImage
from azure.search.documents import SearchClient
from azure.search.documents.models import (
    VectorizedQuery,
    QueryType,
    QueryCaptionType,
    QueryAnswerType,
)
from azure.core.credentials import AzureKeyCredential
from promptflow.connections import (
    CognitiveSearchConnection,
    CustomConnection
)

@tool
def do_search(
    question: str,
    index_name: str,
    #embedding: List[float],
    search: CognitiveSearchConnection,
    vision: CustomConnection,
    image: PFImage = None,
) -> str:
    
    image_vector = None
    if image is not None:
        vector_data = vectorize_image(image, vision.configs["api_base"], vision.secrets["api_key"])
        image_vector = vector_data['vector']

    results = perform_image_search(search, index_name, question, image_vector)

    docs = [
        {
            "description": doc["description"]
        }
        for doc in results
    ]

    return docs

def vectorize_image(image_data, endpoint, subscription_key):
    api_url = f"{endpoint}/computervision/retrieval:vectorizeImage?api-version=2024-02-01&model-version=2023-04-15"
    
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key
    }

    response = requests.post(api_url, headers=headers, data=image_data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

def perform_image_search(search, index_name, text_query, image_vector=None):
    search_client = SearchClient(
        endpoint=search.configs["api_base"],
        index_name=index_name,
        credential=AzureKeyCredential(search.secrets["api_key"]),
    )

    vector_queries = None
    if image_vector is not None:
        vector_queries = [VectorizedQuery(vector=image_vector, k_nearest_neighbors=3, fields="image_vector")]

    results = search_client.search(  
        search_text=text_query,  
        vector_queries=vector_queries,
        select=["description", "filepath"],
    )  
    
    return results