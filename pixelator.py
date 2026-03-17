from email.mime import image
import os   
from skimage.segmentation import slic
import PIL.Image as Image
import numpy as np

class Pixelator:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        
    # def Pixelate(self, image, pixel_size, palette):
    #     # 1. FORCE THE GRID (Downsample)
    #     # This creates the physical "pixels"
    #     width, height = image.size
    #     small_w = max(1, width // pixel_size)
    #     small_h = max(1, height // pixel_size)
    #     small_img = image.resize((small_w, small_h), resample=Image.BILINEAR)
        
    #     # 2. COLOR THE SQUARES
    #     # We process the tiny image. Since it's already tiny, 
    #     # we can use the fast broadcasting math.
    #     pixels = np.array(small_img.convert('RGB')).reshape(-1, 3)
        
    #     # Fast Vectorized Distance
    #     dist_sq = np.sum((pixels[:, np.newaxis, :] - palette)**2, axis=2)
    #     closest_indices = np.argmin(dist_sq, axis=1)
    #     new_pixels = palette[closest_indices]
        
    #     # 3. UPSCALED GRID
    #     # Reshape and blow it back up with NEAREST to keep sharp edges
    #     output_array = new_pixels.reshape(small_h, small_w, 3).astype('uint8')
    #     result = Image.fromarray(output_array)
    #     return result.resize((width, height), resample=Image.NEAREST)
    
    # def Pixelate(self, image, pixel_size, palette=None):
    #     # Open the image using PIL
    #     self.image = Image.open(self.image_path).convert('RGB')
        
    #     width= self.image.width
    #     height= self.image.height
        
    #     # Create a new image to store the pixelated version
    #     pixelated_image = Image.new('RGB', (width, height))
        
    #     small_image= self.image.resize((width // pixel_size, height // pixel_size), resample=Image.NEAREST)
        
    #     pixelated_image = small_image.resize((width, height), resample=Image.NEAREST)
        
    #     if palette is not None: 
    #         pixelated_image = self.apply_palette(pixelated_image, palette=palette)
    #     return pixelated_image
            
            
    # # def apply_palette(self, pixelated_image, palette):
    # #     width, height = pixelated_image.size
    # #     pixels = np.array(pixelated_image).reshape(-1, 3)

    # #          # 1. Broad-casting math: Calculate distances for ALL pixels at once
    # #        # This creates a distance matrix of (num_pixels, num_palette_colors)
    # #     distances = np.sqrt(((pixels[:, np.newaxis, :] - palette)**2).sum(axis=2))

    # #       # 2. Find the index of the smallest distance for each pixel
    # #     closest_indices = np.argmin(distances, axis=1)

    # #  # 3. Map the indices back to palette colors
    # #     new_pixels = palette[closest_indices]

    # #  # 4. Reshape back to image dimensions
    # #     return Image.fromarray(new_pixels.reshape(height, width, 3).astype('uint8'))
    
    def segmentation_sampling(self, image, palette, n_segments=2000):
        img_np = np.array(image.convert('RGB'))
        # Create organic shapes based on color boundaries
        segments = slic(img_np, n_segments=n_segments, compactness=1, start_label=1)
        
        # Color each segment based on the palette
        res = np.zeros_like(img_np)
        for seg_val in np.unique(segments):
            mask = segments == seg_val
            avg_color = img_np[mask].mean(axis=0)
            
            # Find closest palette color for this specific shape
            dist = np.sqrt(((avg_color - palette)**2).sum(axis=1))
            best_color = palette[np.argmin(dist)]
            res[mask] = best_color
            
        return Image.fromarray(res.astype('uint8'))
    
    def grid_sampling(self, image, palette, pixel_size):
        width, height = image.size
        small_width = max(1, width // pixel_size)
        small_height = max(1, height // pixel_size)
        
        small_image = image.resize((small_width, small_height), resample=Image.BOX). convert('RGB')
        # pixels = np.array(small_image).reshape(-1, 3)   
        # dist = np.sqrt(((pixels[:, np.newaxis, :] - palette)**2).sum(axis=2))
        # closest_indices = np.argmin(dist, axis=1)
        # new_pixels = palette[closest_indices]
        # output_array = new_pixels.reshape(small_height, small_width, 3).astype('uint8')
        # return Image.fromarray(output_array).resize((width, height), resample=Image.NEAREST)   
        
        new_pixels=np.zeros_like(np.array(small_image))
        pixels= np.array(small_image)
        
        for i in range(small_height):
            for j in range(small_width):
                pixel_color= pixels[i, j]
                best_color= palette[np.argmin(np.sqrt(((pixel_color - palette)**2).sum(axis=1)))]
                
                new_pixels[i, j]= best_color
                
        return Image.fromarray(new_pixels.astype('uint8')).resize((width, height), resample=Image.NEAREST)
                
    