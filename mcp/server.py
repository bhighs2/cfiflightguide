import os

from dotenv import load_dotenv
from mcp.server import MCPServer
from openai import OpenAI


load_dotenv()

VECTOR_STORE_ID = os.environ["OPENAI_APPROVED_VECTOR_STORE_ID"]

client = OpenAI()
mcp = MCPServer("Flight Guide Knowledge Base")


@mcp.tool()
def search_flight_guide(query: str, max_results: int = 8) -> str:
    """Search the Flight Guide OpenAI vector store."""

    query = query.strip()

    if not query:
        return "A search query is required."

    max_results = max(1, min(max_results, 20))

    results = client.vector_stores.search(
        vector_store_id=VECTOR_STORE_ID,
        query=query,
        max_num_results=max_results,
    )

    if not results.data:
        return f"No vector-store results found for: {query}"

    output = []

    for index, result in enumerate(results.data, start=1):
        text_parts = []

        for content in result.content:
            text = getattr(content, "text", None)
            if text:
                text_parts.append(text)

        chunk_text = "\n".join(text_parts)

        output.append(
            f"""RESULT {index}
SOURCE: {result.filename}
RELEVANCE: {result.score:.3f}

{chunk_text}"""
        )

    return "\n\n---\n\n".join(output)


if __name__ == "__main__":
    mcp.run()