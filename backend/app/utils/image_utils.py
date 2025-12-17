# utils/image_utils.py
from PIL import Image
import numpy as np

def preprocess_xray(image_path: str):
    img = Image.open(image_path).convert("L").resize((224, 224))
    return np.array(img) / 255.0