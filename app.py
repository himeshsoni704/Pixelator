# from flask import Flask, render_template, request
# import PIL.Image as Image
# import os


# from pixelator import Pixelator
# from swatch import swatch
# app = Flask(__name__, template_folder=r'/home/himesh/CODE_FILES/pixelator', static_folder=r'/home/himesh/CODE_FILES/pixelator')


# @app.route('/')
# def pixelate():
#     return render_template('index.html')

# def hex_to_rgb(self, hex_color):
#         hex_color = hex_color.lstrip('#')
#         a=[]
#         for i in (0,2,4):
#             a.append(int(hex_color[i:i+2], 16))
#         return tuple(a)

# @app.route('/upload', methods=['POST'])
# def upload():
#     file= request.files['file']
#     if file:
#         filename = file.filename
#         file.save(file.filename)
        
        
#         # 2. Get the size from the saved file instead of the stream
#         file_size = os.path.getsize(file.filename)
#         print(f"Received image: {file_size / 1024:.2f} KB")
#         # Open the image using PIL
#         # In your upload route, before pixelating:
#         image = Image.open(file.filename)
#         if image.width > 1000:
#             image = image.resize((1000, int(1000 * image.height / image.width)), resample=Image.LANCZOS)
        
#         print(f"Image format: {image.format}, size: {image.size}, mode: {image.mode}")
        
#         pallete_extractor= swatch(color=None, count=None)
#         pixelator= Pixelator(image_path=file.filename)
        
#         swatches= pallete_extractor.extract_palette(image, num_colors=4)
        
        
#         mode= request.form.get('mode')
#         pixel_size= int(request.form.get('pixel_size', 10))
#         pallete_type= request.form.get('palette_type')
        
                    
#         if palette_type == 'custom':
#             # Collect all hex codes from the 8 pickers
#             #hex_colors = request.form.getlist('custom_colors')
#             colors = request.form.getlist('custom_colors')
#             # Convert to RGB numpy array for the Pixelator
#             swatches = np.array([hex_to_rgb(c) for c in hex_colors])
#         else:
#             # Your existing auto-extract logic
#             extractor = swatch(color=None, count=None)
#             swatches = extractor.extract_palette(image, num_colors=8)
            
#         if mode=='Segment':
#             pixelated= pixelator.segmentation_sampling(image, palette=swatches, n_segments=2000)
#         else: 
#             pixelated= pixelator.grid_sampling(image, pixel_size=6, palette=swatches)

#     # Pixelate
#     pixelator = Pixelator(image_path=img_path)
#     if mode == 'Segment':
#         # Map pixel_size to n_segments (smaller pixel size = more segments)
#         n_segs = max(100, 5000 // pixel_size) 
#         pixelated = pixelator.segmentation_sampling(image, palette=swatches, n_segments=n_segs)
#     else:
#         pixelated = pixelator.grid_sampling(image, palette=swatches, pixel_size=pixel_size)
            
            
#         filename = "output.png"
#         pixelated.save(filename)

#         return render_template(
#             'uploaded.html',
#             filename=filename,
#             swatches=swatches)
    
#     return 'No file uploaded', 400
    
    
    
# if __name__ == '__main__':
#     app.run(host="0.0.0.0",port=5050)




from flask import Flask, render_template, request
import PIL.Image as Image
import os
import numpy as np
from pixelator import Pixelator
from swatch import swatch

app = Flask(__name__, template_folder=r'/home/himesh/CODE_FILES/pixelator', static_folder=r'/home/himesh/CODE_FILES/pixelator')

# Helper function (outside the route)
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return 'No file uploaded', 400

    filename = file.filename
    img_path = os.path.join(app.static_folder, filename)
    file.save(img_path)

    # Open and resize image
    image = Image.open(img_path)
    if image.width > 1000:
        new_height = int(1000 * image.height / image.width)
        image = image.resize((1000, new_height), resample=Image.LANCZOS)
    
    # Get form data
    mode = request.form.get('mode')
    pixel_size = int(request.form.get('pixel_size', 10))
    # FIX: Use consistent spelling 'palette_type'
    palette_type = request.form.get('palette_type')

    # Handle Palette Selection
    if palette_type == 'custom':
        hex_colors = request.form.getlist('custom_colors')
        # Convert to RGB numpy array
        swatches = np.array([hex_to_rgb(c) for c in hex_colors if c])[:16]  # Limit to 16 colors
    else:
        # Auto-extract logic
        pallete_extractor = swatch(color=None, count=None)
        swatches = pallete_extractor.extract_palette(image, num_colors=22)

    # Initialize Pixelator
    pixelator = Pixelator(image_path=img_path)
    
    # Process Image based on Mode
    if mode == 'Segment':
        # Smaller pixel_size slider value = more segments (higher detail)
        n_segs = max(200, 8000 // pixel_size) 
        pixelated = pixelator.segmentation_sampling(image, palette=swatches, n_segments=n_segs)
    else:
        pixelated = pixelator.grid_sampling(image, palette=swatches, pixel_size=pixel_size)

    # Save output
    output_filename = "output.png"
    output_path = os.path.join(app.static_folder, output_filename)
    pixelated.save(output_path)

    return render_template('uploaded.html', filename=output_filename, swatches=swatches)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)