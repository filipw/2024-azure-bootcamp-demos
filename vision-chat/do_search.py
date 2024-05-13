import os
import requests
from typing import List
from promptflow.core import tool
from azure.search.documents import SearchClient
from azure.search.documents.models import (
    VectorizedQuery,
    QueryType,
    QueryCaptionType,
    QueryAnswerType,
)
from azure.core.credentials import AzureKeyCredential
from promptflow.connections import CognitiveSearchConnection

@tool
def do_search(
    question: str,
    index_name: str,
    search: CognitiveSearchConnection,
    image_vector: List[float],
) -> str:
    search_client = SearchClient(
        endpoint=search.configs["api_base"],
        index_name=index_name,
        credential=AzureKeyCredential(search.secrets["api_key"]),
    )

    vector_queries = None
    if image_vector:
        vector_queries = [VectorizedQuery(vector=image_vector, k_nearest_neighbors=3, fields="image_vector")]

    results = search_client.search(  
        top=5,
        search_text=question,  
        vector_queries=vector_queries,
        select=["description", "filepath"],
    )  
    
    docs = [
        {
            "description": doc["description"],
            "score": doc["@search.score"]
        }
        for doc in results
    ]

    return docs