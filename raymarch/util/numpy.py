import numpy as np


def normalize(vector: np.ndarray) -> None:
    """
    normalize vector (in-place)
    :param vector: vector to normalize
    """
    norm = np.linalg.norm(vector)
    if norm != 0:
        vector /= np.linalg.norm(vector)


def normalized(vector: np.ndarray) -> np.ndarray:
    """
    :param vector: vector to normalize
    :return: normalized version of vector
    """
    norm = np.linalg.norm(vector)
    if norm != 0:
        return vector.copy() / np.linalg.norm(vector)
    else:
        return vector.copy()
