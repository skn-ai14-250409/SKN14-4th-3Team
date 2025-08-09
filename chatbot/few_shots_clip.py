from django.conf import settings
import torch
from PIL import Image
import numpy as np

from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity


# EMB_DIR = os.path.join(settings.BASE_DIR, "suppport_embeddings.npy")
EMB_DIR = settings.BASE_DIR/"support_embeddings.npy"



device = "cuda" if torch.cuda.is_available() else "cpu"

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_clip_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
    return image_features[0].cpu().numpy()  # shape: (512,)



# 사전 저장된 임베딩 로드
class_embeddings = np.load(EMB_DIR, allow_pickle=True).item()
def predict_model(image_path):
    emb = get_clip_embedding(image_path).reshape(1, -1)
    labels = list(class_embeddings.keys())
    vectors = np.array([class_embeddings[label] for label in labels])
    
    sims = cosine_similarity(emb, vectors)[0]
    top_idx = np.argmax(sims)
    return labels[top_idx], sims[top_idx]

