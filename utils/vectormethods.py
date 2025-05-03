import numpy as np

def clamp_magnitude(vec, max_length):
        norm = np.linalg.norm(vec)
        if norm > max_length:
            return vec / norm * max_length
        return vec

def normalize(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def distance(pos1, pos2):
    return np.linalg.norm(pos1 - pos2)


def facingDirection(vel):
    if np.linalg.norm(vel) != 0:
        return normalize(vel)
    else:
        return np.array([0, -1])


def angle_between(vec1, vec2):
    v1_u = normalize(vec1)
    v2_u = normalize(vec2)
    dot_product = np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)
    angle_rad = np.arccos(dot_product)
    angle_deg = np.degrees(angle_rad)
    return angle_deg

def inverse(vec):
    return normalize(-vec)

def rotateVector(vector, degrees):
    radians = np.deg2rad(degrees)
    rotation_matrix = np.array([
        [np.cos(radians), -np.sin(radians)],
        [np.sin(radians), np.cos(radians)]
    ])
    return np.dot(rotation_matrix, vector)
