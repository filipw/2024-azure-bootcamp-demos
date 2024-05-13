from promptflow.core import tool

@tool
def fetch_user_data(user_id: int) -> str:
  if user_id == 1:
    return 'Filip'

  return 'Goofy'