import requests
from typing import List
from promptflow.core import tool
from promptflow.contracts.multimedia import Image as PFImage
from promptflow.connections import CustomConnection
from utils import is_valid

@tool
def vectorize_image(vision: CustomConnection, image: PFImage = None) -> List[float]:
    if image is not None and is_valid(image):
        endpoint = vision.configs["api_base"]
        subscription_key = vision.secrets["api_key"]
        api_url = f"{endpoint}/computervision/retrieval:vectorizeImage?api-version=2024-02-01&model-version=2023-04-15"
        
        headers = {
            "Content-Type": "application/octet-stream",
            "Ocp-Apim-Subscription-Key": subscription_key
        }

        response = requests.post(api_url, headers=headers, data=image)

        if response.status_code == 200:
            vector_data = response.json()
            return vector_data['vector']
        else:
            raise Exception(f"API call failed with status code {response.status_code}: {response.text}")
    
    return []