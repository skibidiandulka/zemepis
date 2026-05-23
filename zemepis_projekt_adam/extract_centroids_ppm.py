#!/usr/bin/env python3
"""
Extract country polygon centroids from world map image.
Using PPM format which is easy to parse.
"""

import json

def read_ppm(filename):
    """Read PPM file and return grayscale image data."""
    with open(filename, 'rb') as f:
        # Read header
        magic = f.readline().strip()
        if magic != b'P6':
            raise ValueError(f"Not a PPM file (P6 format): {magic}")

        # Skip comments
        while True:
            line = f.readline()
            if not line.startswith(b'#'):
                break

        # Parse dimensions from the line we just read
        dims = line.strip().split()
        width, height = int(dims[0]), int(dims[1])

        # Read max color value
        maxval = int(f.readline().strip())

        print(f"PPM: {width}x{height}, maxval={maxval}")

        # Read pixel data
        pixels = []
        for y in range(height):
            if y % 200 == 0:
                print(f"Reading row {y}/{height}...")
            row = []
            for x in range(width):
                r = ord(f.read(1))
                g = ord(f.read(1))
                b = ord(f.read(1))
                # Convert to grayscale
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                row.append(gray)
            pixels.append(row)

        return pixels, width, height


def flood_fill(binary_img, start_y, start_x, visited, width, height):
    """Simple flood fill to find connected regions."""
    stack = [(start_y, start_x)]
    region_pixels = []

    while stack:
        y, x = stack.pop()

        if y < 0 or y >= height or x < 0 or x >= width:
            continue
        if visited[y][x] or not binary_img[y][x]:
            continue

        visited[y][x] = True
        region_pixels.append((y, x))

        # Add 4-connected neighbors
        stack.append((y-1, x))
        stack.append((y+1, x))
        stack.append((y, x-1))
        stack.append((y, x+1))

    return region_pixels


def find_country_polygons(gray_pixels, width, height, threshold=100, min_area=500):
    """Find distinct country polygons using flood fill."""
    print("Creating binary mask...")
    # Create binary mask
    binary = [[pixel > threshold for pixel in row] for row in gray_pixels]
    visited = [[False] * width for _ in range(height)]

    polygons = []

    print("Scanning for regions...")
    # Scan through image to find unvisited land pixels
    for y in range(height):
        if y % 200 == 0:
            print(f"Scanning row {y}/{height}... (found {len(polygons)} regions so far)")
        for x in range(width):
            if binary[y][x] and not visited[y][x]:
                # Found new region - flood fill it
                region_pixels = flood_fill(binary, y, x, visited, width, height)

                if len(region_pixels) >= min_area:
                    # Calculate centroid
                    sum_y = sum(p[0] for p in region_pixels)
                    sum_x = sum(p[1] for p in region_pixels)
                    cy = int(sum_y / len(region_pixels))
                    cx = int(sum_x / len(region_pixels))

                    polygons.append({
                        'centroid_x': cx,
                        'centroid_y': cy,
                        'area': len(region_pixels)
                    })
                    print(f"  Found region #{len(polygons)}: area={len(region_pixels)}, centroid=({cx},{cy})")

    return polygons


def pixel_to_latlon(x, y, img_width, img_height):
    """Convert pixel coordinates to latitude/longitude."""
    lon = (x / img_width) * 360 - 180
    lat = 90 - (y / img_height) * 180
    return lat, lon


def extract_centroids(image_path, min_area=500):
    """Main function to extract all country centroids."""
    print(f"Loading image: {image_path}")

    # Load image
    pixels, width, height = read_ppm(image_path)
    print(f"Image loaded: {width}x{height}")

    # Find polygons
    polygons = find_country_polygons(pixels, width, height, threshold=100, min_area=min_area)
    print(f"\nFound {len(polygons)} polygons with area >= {min_area} pixels")

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
    image_path = '/tmp/earth.ppm'

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
