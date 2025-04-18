from __future__ import annotations

from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel


def embed_text(texts: list[str]) -> list[list[float]]:
    """Embeds texts with a pre-trained, foundational model.

    Returns:
        A list of lists containing the embedding vectors for each input text
    """

    # A list of texts to be embedded.

    # The dimensionality of the output embeddings.
    dimensionality = 256
    # The task type for embedding. Check the available tasks in the model's documentation.
    task = "RETRIEVAL_DOCUMENT"

    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    inputs = [TextEmbeddingInput(text, task) for text in texts]
    kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
    embeddings = model.get_embeddings(inputs, **kwargs)

    print(embeddings)
    # Example response:
    # [[0.006135190837085247, -0.01462465338408947, 0.004978656303137541, ...], [0.1234434666, ...]],
    return [embedding.values for embedding in embeddings]



if __name__ == "__main__":
    # Code in this block will only run when the script is executed directly
    texts = ["banana muffins? ", "banana bread? banana muffins?"]

    embeddings = embed_text(texts)
    print(embeddings)
