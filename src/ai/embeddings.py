import numpy as np, hashlib, json

DIM = 384

def _hash_to_vec(s: str, dim: int = DIM) -> np.ndarray:
    h = hashlib.sha256(s.encode()).digest()
    # repete bytes para preencher o vetor
    arr = np.frombuffer(h * ((dim // len(h)) + 1), dtype=np.uint8)[:dim].astype(np.float32)
    # normaliza para unit-length
    arr /= (np.linalg.norm(arr) + 1e-9)
    return arr

def embed_text(text: str) -> np.ndarray:
    return _hash_to_vec(text)

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / ((np.linalg.norm(a) + 1e-9) * (np.linalg.norm(b) + 1e-9)))

def to_storage(vec: np.ndarray) -> str:
    return json.dumps(vec.tolist())

def from_storage(s: str) -> np.ndarray:
    return np.array(json.loads(s), dtype=np.float32)
