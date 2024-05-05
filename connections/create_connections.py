import os
from pathlib import Path

from promptflow.client import PFClient
from promptflow.entities import (
    AzureOpenAIConnection,
    CustomConnection,
    CognitiveSearchConnection,
)
from dotenv import load_dotenv

load_dotenv()

pf = PFClient()

AZURE_OPENAI_KEY= os.environ["AZURE_OPENAI_KEY"]
AZURE_OPENAI_RESOURCE= os.environ["AZURE_OPENAI_RESOURCE"]
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION") or "2024-02-15-preview"
connection = AzureOpenAIConnection(
    name="open_ai_connection",
    api_key=AZURE_OPENAI_KEY,
    api_base=f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/",
    api_type="azure",
    api_version=API_VERSION,
)

print(f"Creating connection {connection.name}...")
result = pf.connections.create_or_update(connection)
print(result)

AZURE_AI_SEARCH_ENDPOINT = os.environ["AZURE_AI_SEARCH_ENDPOINT"]
AZURE_AI_SEARCH_KEY = os.environ["AZURE_AI_SEARCH_KEY"]
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION") or "2024-03-01-preview"
connection = CognitiveSearchConnection(
    name="ai_search_connection",
    api_key=AZURE_AI_SEARCH_KEY,
    api_base=AZURE_AI_SEARCH_ENDPOINT,
    api_version=API_VERSION,
)

print(f"Creating connection {connection.name}...")
result = pf.connections.create_or_update(connection)
print(result)

AZURE_VISION_ENDPOINT = os.environ["AZURE_VISION_ENDPOINT"]
AZURE_VISION_KEY = os.environ["AZURE_VISION_KEY"]
connection = CustomConnection(
    name="vision_connection",
    configs={"api_base": AZURE_VISION_ENDPOINT},
    secrets={"api_key": AZURE_VISION_KEY},
)
print(f"Creating connection {connection.name}...")
result = pf.connections.create_or_update(connection)
print(result)