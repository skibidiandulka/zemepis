#!/usr/bin/env python3
"""
Extract country polygon centroids from world map image.
"""

from PIL import Image
import numpy as np
import json
from scipy import ndimage
from skimage import measure

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
    # Using threshold to separate land (bright) from ocean (dark)
    binary = gray > 100

    return binary

def find_country_polygons(binary_img, min_area=500):
    """Find distinct country polygons using connected components."""
    # Label connected components
    labeled, num_features = ndimage.label(binary_img)

    # Find regions and calculate centroids
    polygons = []
    for region_id in range(1, num_features + 1):
        # Create mask for this region
        region_mask = (labeled == region_id)
        area = np.sum(region_mask)

        if area >= min_area:
            # Calculate centroid
            coords = np.argwhere(region_mask)
            cy = int(np.mean(coords[:, 0]))
            cx = int(np.mean(coords[:, 1]))

            polygons.append({
                'centroid_x': cx,
                'centroid_y': cy,
                'area': area
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
