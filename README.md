# Faces-To-Panorama
Simple python tool that turns 6 faces (.png) from a .zip file into a single panorama texture (.png)

# ZIP → Panorama Tool

A simple python tool (tested in Python 3.13) that converts a ZIP archive containing six cubemap face images into a single panorama texture.

Designed specifically for fast panorama preparation for **Flax Engine** but could be useful elsewhere.

---

## Requirements

- **Python 3.13.5+**
- Pillow (PIL fork)
- Numpy

Install Pillow:

```bash
pip install pillow
pip install numpy
```

---

## Features

- Accepts a `.zip` file containing cubemap faces
- Validates required images and resolutions
- Outputs a **single stitched panorama image**
- Minimal dependencies
- Fails fast on errors

---

## Required Input Files

The ZIP archive **must contain exactly these files**:

```
front.png
back.png
left.png
right.png
top.png
bottom.png

```

### Rules
- All images **must be PNG**
- All images **must be the same resolution**
- File names are **case-sensitive**

---

## Usage

```bash
python zip_to_panorama.py input.zip output.png
```

### Example

```bash
python zip_to_panorama.py skybox.zip skybox_panorama.png
```

---

## Error Handling

The tool will stop with a clear error if:

- A required face image is missing
- Image resolutions do not match
- The ZIP file cannot be read

---

## Notes

- No image rotation is applied — face orientation must already be correct
- Alpha channel is preserved
- Output format is PNG (lossless)

---

## Possible Extensions

If needed, this tool can be extended to support:
- DDS export
- Vertical cross layout
- Face rotation correction
- Batch processing
- CLI installation via `pip`

---

## License

MIT License

Copyright (c) 2025 ilex

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
