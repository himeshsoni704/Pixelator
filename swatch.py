from email.mime import image
from skimage.segmentation import slic
import os
import PIL.Image as Image
from fastapi import requests
import numpy as np
from sklearn.cluster import KMeans

class swatch:
    def __init__(self, color, count):
        self.color = color
        self.count = count
    
    # def extract_palette(self, image, num_colors):
        
    #     small_image= image.resize(image.size, resample=Image.NEAREST)
    #     pixels = np.array(small_image)
    #     pixels = pixels.reshape(-1, 3)
    #     unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    #     from sklearn.cluster import KMeans
    #     kmeans = KMeans(n_clusters=num_colors, random_state=0).fit(unique_colors)
    #     palette = kmeans.cluster_centers_.astype(int)
    #     return palette
    
    # def request_ai_swatches(self, image, num_colors):
    #     buffer=io.BytesIO()
    #     image.save(buffer, format='PNG')
    #     buffer.seek(0)
    #     files = {'file': ('image.png', buffer, 'image/png')}
    #     payload = {'num_colors': num_colors}
    #     response = requests.post('http://localhost:8000/extract_palette', files=files, data=payload)
        
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         print(f"Error: {response.status_code}")
    #         return None
        
        
    
    def extract_palette(self, image, num_colors):
        img_np = np.array(image.convert('RGB'))
    
    # 1. Use SLIC to find segments (shapes)
        segments = slic(img_np, n_segments=1000, compactness=2)
    
    # 2. Get the average color of each segment
        segment_colors = []
        for seg_val in np.unique(segments):
             mask = segments == seg_val
             segment_colors.append(img_np[mask].mean(axis=0))
    
    # 3. Run KMeans on the SHAPES, not the pixels
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=num_colors, random_state=0).fit(segment_colors)
        return kmeans.cluster_centers_.astype(int)