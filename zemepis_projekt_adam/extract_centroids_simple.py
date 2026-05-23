#!/usr/bin/env python3
"""
Extract country polygon centroids from world map image.
Simple version using only PIL and numpy.
"""

from PIL import Image
import numpy as np
import json

def load_image(image_path):
    """Load the world map image."""
    img = Image.open(image_path)
    return np.array(img)

def preprocess_image(img):
    """Convert to grayscale and create binary mask for land areas."""
    # Convert to grayscale if needed
    if len(img.shape) == 3:
        # Convert RGB to grayscale
        gray = np.mean(img, axis=2).astype(np.uint8)
    else:
        gray = img

    # Create binary mask - land is white/light gray, ocean is blue (dark)
    binary = gray > 100

    return binary

def flood_fill(binary_img, start_y, start_x, visited):
    """Simple flood fill to find connected regions."""
    height, width = binary_img.shape
    stack = [(start_y, start_x)]
    region_pixels = []

    while stack:
        y, x = stack.pop()

        if y < 0 or y >= height or x < 0 or x >= width:
            continue
        if visited[y, x] or not binary_img[y, x]:
            continue

        visited[y, x] = True
        region_pixels.append((y, x))

        # Add 4-connected neighbors
        stack.append((y-1, x))
        stack.append((y+1, x))
        stack.append((y, x-1))
        stack.append((y, x+1))

    return region_pixels

def find_country_polygons(binary_img, min_area=500):
    """Find distinct country polygons using flood fill."""
    height, width = binary_img.shape
    visited = np.zeros((height, width), dtype=bool)
    polygons = []

    # Scan through image to find unvisited land pixels
    for y in range(height):
        for x in range(width):
            if binary_img[y, x] and not visited[y, x]:
                # Found new region - flood fill it
                region_pixels = flood_fill(binary_img, y, x, visited)

                if len(region_pixels) >= min_area:
                    # Calculate centroid
                    ys = [p[0] for p in region_pixels]
                    xs = [p[1] for p in region_pixels]
                    cy = int(np.mean(ys))
                    cx = int(np.mean(xs))

                    polygons.append({
                        'centroid_x': cx,
                        'centroid_y': cy,
                        'area': len(region_pixels)
                    })

    return polygons

def pixel_to_latlon(x, y, img_width, img_height):
    """Convert pixel coordinates to latitude/longitude."""
    lon = (x / img_width) * 360 - 180
    lat = 90 - (y / img_height) * 180
    return lat, lon

def extract_centroids(image_path, min_area=500):
    """Main function to extract all country centroids."""
    # Load and process image
    img = load_image(image_path)
    height, width = img.shape[:2]

    print(f"Image dimensions: {width}x{height}")

    # Preprocess
    binary = preprocess_image(img)
    print(f"Binary mask created, scanning for regions...")

    # Find polygons
    polygons = find_country_polygons(binary, min_area)

    print(f"Found {len(polygons)} polygons with area >= {min_area} pixels")

    # Convert to output format
    results = []
    for idx, poly in enumerate(polygons, start=1):
        x = poly['centroid_x']
        y = poly['centroid_y']
        lat, lon = pixel_to_latlon(x, y, width, height)

        results.append({
            'id': idx,
            'pixel_x': x,
            'pixel_y': y,
            'lat': round(lat, 4),
            'lon': round(lon, 4),
            'approximate_area': int(poly['area'])
        })

    # Sort by area (largest first)
    results.sort(key=lambda x: x['approximate_area'], reverse=True)

    # Reassign IDs after sorting
    for idx, item in enumerate(results, start=1):
        item['id'] = idx

    return results

if __name__ == '__main__':
    image_path = '/var/www/zemepis/textures/earth.png'

    try:
        centroids = extract_centroids(image_path, min_area=500)

        # Output as JSON
        output = json.dumps(centroids, indent=2)
        print("\n" + "="*80)
        print("RESULTS:")
        print("="*80)
        print(output)

        # Also save to file
        output_file = '/home/andulkapilulka/zemepis_projekt_adam/country_centroids.json'
        with open(output_file, 'w') as f:
            f.write(output)
        print(f"\n\nResults saved to: {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
