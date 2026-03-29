import os
from cerebras.cloud.sdk import Cerebras

# Replace with your actual API key
client = Cerebras(api_key="csk-wxetrf9w4hnp948e42ex3rw98ch4yh68jne85twrjwvjnhnt")

models = client.models.list()

print("Available Models:")
for model in models.data:
    print(f"- {model.id} (Owned by: {model.owned_by})")