import zipfile
import tempfile
import sys
import math
from pathlib import Path

import numpy as np
from PIL import Image

FACES = {
    "right.png":  +1,
    "left.png":   -1,
    "top.png":    +2,
    "bottom.png": -2,
    "front.png":  +3,
    "back.png":   -3,
}

def load_faces(folder: Path):
    faces = {}
    for name in FACES:
        path = folder / name
        if not path.exists():
            raise FileNotFoundError(f"Missing {name}")
        faces[name] = Image.open(path).convert("RGB")
    return faces

def cubemap_direction(face, u, v):
    if face == +1:   # +X right
        return np.array([1, v, -u])
    if face == -1:   # -X left
        return np.array([-1, v, u])
    if face == +2:   # +Y top
        return np.array([u, 1, -v])
    if face == -2:   # -Y bottom
        return np.array([u, -1, v])
    if face == +3:   # +Z front
        return np.array([u, v, 1])
    if face == -3:   # -Z back
        return np.array([-u, v, -1])

def sample_cubemap(faces, direction):
    x, y, z = direction
    ax, ay, az = abs(x), abs(y), abs(z)

    if ax >= ay and ax >= az:
        face = "right.png" if x > 0 else "left.png"
        u = -z / ax if x > 0 else z / ax
        v = y / ax
    elif ay >= ax and ay >= az:
        face = "top.png" if y > 0 else "bottom.png"
        u = x / ay
        v = -z / ay if y > 0 else z / ay
    else:
        face = "front.png" if z > 0 else "back.png"
        u = x / az if z > 0 else -x / az
        v = y / az

    img = faces[face]
    w, h = img.size

    px = int((u * 0.5 + 0.5) * (w - 1))
    py = int((v * 0.5 + 0.5) * (h - 1))

    return img.getpixel((px, h - py - 1))

def cubemap_to_panorama(faces, width, height):
    pano = Image.new("RGB", (width, height))
    pixels = pano.load()

    for y in range(height):
        v = y / height
        theta = v * math.pi

        for x in range(width):
            u = x / width
            phi = u * 2 * math.pi

            direction = np.array([
                math.sin(theta) * math.sin(phi),
                math.cos(theta),
                math.sin(theta) * math.cos(phi),
            ])

            color = sample_cubemap(faces, direction)
            pixels[x, y] = color

    return pano

def main(zip_path, output_path, width=4096):
    zip_path = Path(zip_path)
    output_path = Path(output_path)

    height = width // 2

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(tmp)

        faces = load_faces(tmp)
        panorama = cubemap_to_panorama(faces, width, height)
        panorama.save(output_path)

        print("✔ Panorama created")
        print(f"Resolution: {width}x{height}")
        print(f"Saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python cubemap_zip_to_panorama.py input.zip output.png [width]")
        sys.exit(1)

    w = int(sys.argv[3]) if len(sys.argv) > 3 else 4096
    main(sys.argv[1], sys.argv[2], w)
