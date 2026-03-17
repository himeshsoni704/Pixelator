# PIXELATOR

Turn any photo into pixel art — right in your browser. Upload an image, pick a style and palette, and get a pixelated version back in seconds.

---

## Table of Contents

1. [What It Does](#what-it-does)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [How to Use](#how-to-use)
5. [Pixelation Modes](#pixelation-modes)
6. [Colour Palettes](#colour-palettes)
7. [Known Limitations](#known-limitations)

---

## What It Does

Pixelator is a local web app that runs on your machine. You open it in a browser, drop in a photo, tweak a few settings, and hit **Execute** — it spits out a pixel-art version of that image. No cloud, no subscriptions, no sign-in.

The landing page has a parallax scroll effect and a pixel-particle animation. Scroll down to reach the workspace where you do everything.

---

## Features

- **Two pixelation styles** — a classic sharp pixel grid, or an organic shape-aware mode that follows the contours of the image
- **Resolution slider** — smoothly dial in how blocky or detailed you want the output
- **Smart auto-palette** — automatically pulls the most fitting colours out of your image
- **Custom 16-colour palette** — build your own palette with colour pickers
- **7 built-in palette presets** — one click to load a full themed palette
- **Drag-and-drop upload** — just drop your image onto the page
- **Instant preview** — result appears at the top of the page right after processing

---

## Getting Started

You need Python installed (3.10 or newer).

```bash
# 1. Get the code
git clone <repo-url>
cd pixelator

# 2. Set up a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py
```

Then open **http://localhost:5050** in your browser.

---

## How to Use

1. Open the app and **scroll down** — the workspace slides in from below.
2. **Drop or click** to upload a JPEG or PNG photo.
3. Pick a **Pixelation Mode** (see below).
4. Drag the **Resolution Scale** slider — left for fine detail, right for chunky blocks.
5. Choose a **Palette Source**:
   - *Auto-extract* — Pixelator figures out the best colours automatically.
   - *Custom Palette* — pick your own colours or load a preset.
6. Hit **EXECUTE\_UPLOAD**.
7. The pixelated result appears at the top. Scroll up to see it, or right-click to save.

---

## Pixelation Modes

### Grid Sampling
The image is broken into a uniform rectangular grid. Every cell becomes one flat colour — the closest match in the palette. This gives the clean, blocky look you'd expect from classic 8-bit games.

Best for: portraits, simple landscapes, anything where you want that retro game aesthetic.

### Organic SLIC
Instead of a rigid grid, the image is divided into regions that follow its natural colour boundaries — edges, shapes, and gradients. Each region gets filled with its closest palette colour. The result is more painterly and less "griddy".

Best for: detailed photos, illustrations, or when you want the pixelation to feel more artistic.

---

## Colour Palettes

### Auto-Extract
Pixelator analyses the image and automatically picks 22 colours that best represent it. These are derived from the image's own tones, so the output always feels cohesive.

### Custom Palette
Switch to *Custom Palette* to reveal 16 colour pickers — set each one to whatever colour you want. The output will only use those shades.

### Quick Presets
Load a themed palette in one click. The pickers update automatically and a colour strip previews the palette instantly.

| Preset | Vibe |
|---|---|
| **CYBERPUNK** | Neons — electric pinks, cyans, yellows |
| **GAMEBOY** | The original 4-shade green |
| **MONO** | Clean 16-step greyscale |
| **NEON** | Vivid fluorescents |
| **PASTEL** | Soft pinks, lavenders, creams |
| **EARTH** | Warm browns and sandy tones |
| **FRUTIGER AERO** | Early-2000s sky blues and teals |

---

## Known Limitations

- **One output at a time** — the result file is overwritten on every upload, so it's designed for one person using it locally.
- **Images over 1000 px wide** are automatically scaled down before processing to keep things fast.
- **Uploaded source images aren't cleaned up** — they accumulate in the project folder until you delete them manually.
