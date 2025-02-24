from secret_ai_sdk.secret_ai import ChatSecret
from secret_ai_sdk.secret import Secret
# load from environment variables or from a .env file
from dotenv import load_dotenv
load_dotenv()

# Create a Secret object to interact with the Secret Network
secret_client = Secret()
# Get all the models registered with the smart contracts
models = secret_client.get_models()
# For the chosen model, you may obtain a list of LLM instance URLs to connect to
urls = secret_client.get_urls(model=models[0])
# You previously exported the env var SECRET_AI_API_KEY=YOUR-API-KEY
secret_ai_llm = ChatSecret(
    base_url=urls[0],  # in this case, we choose to access the first URL in the list
    model=models[0],  # your previously selected model
    temperature=0,  # set the temperature to 0 for deterministic results
)
# Define your messages to send to the confidential LLM for processing
messages = [
    ("system", "You are a helpful assistant that translates English to French. Translate the user sentence."),
    ("human", "I love programming."),
]
# Invoke the LLM
response = secret_ai_llm.invoke(messages, stream=False)
print(response.content)
