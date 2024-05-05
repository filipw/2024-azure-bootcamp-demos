from promptflow.core import tool

@tool
def fetch_user_data(user_id: int) -> str:
  return 'filip'