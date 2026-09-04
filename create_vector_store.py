from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

vector_store = client.vector_stores.create(
    name="APPROVED_AVIATION_SOURCES"
)

print("Vector Store created")
print("Name:", vector_store.name)
print("ID:", vector_store.id)