import numpy as np


def cosine(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
