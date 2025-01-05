import numpy as np
from typing import List


def collaborative_filtering_similarity(
    company_attributes: List[float], candidate_attributes: List[float]
) -> float:
    """
    Compute the similarity score between a company and a candidate using collaborative filtering.

    :param company_attributes: List of company attribute scores (-1 to 1)
    :param candidate_attributes: List of candidate attribute scores (-1 to 1)
    :return: Similarity score between -1 and 1
    """
    if len(company_attributes) != len(candidate_attributes):
        raise ValueError(
            "Company and candidate attribute lists must have the same length"
        )

    # Convert lists to numpy arrays for efficient computation
    company_vector = np.array(company_attributes)
    candidate_vector = np.array(candidate_attributes)

    # Compute cosine similarity
    dot_product = np.dot(company_vector, candidate_vector)
    company_magnitude = np.linalg.norm(company_vector)
    candidate_magnitude = np.linalg.norm(candidate_vector)

    # Avoid division by zero
    if company_magnitude == 0 or candidate_magnitude == 0:
        return 0

    similarity = dot_product / (company_magnitude * candidate_magnitude)

    return similarity
