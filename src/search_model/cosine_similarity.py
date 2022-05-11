import numpy as np


# Module for calculating cosine similarity

def cosine_similarity(vec_a: np.array, vec_b: np.array) -> float:
    """
    Calculates the cosine similarity between two documents
    :param vec_a: The vector of the first document - e.g. a query
    :param vec_b: The vector of the second document - e.g. a document in the index
    :return:
    """
    return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
