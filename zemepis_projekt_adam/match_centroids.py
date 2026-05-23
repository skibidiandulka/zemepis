#!/usr/bin/env python3
import json
import math

# Read the auto-detected centroids
with open('/home/andulkapilulka/zemepis_projekt_adam/country_centroids.json', 'r', encoding='utf-8') as f:
    centroids = json.load(f)

# Read the existing countries with names
with open('/var/www/zemepis/data/countries_averaged.json', 'r', encoding='utf-8') as f:
    countries = json.load(f)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate simple Euclidean distance between two lat/lon points"""
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def find_closest_centroid(country_lat, country_lon, centroids):
    """Find the closest centroid to the given country position"""
    min_distance = float('inf')
    closest_centroid = None

    for centroid in centroids:
        distance = calculate_distance(country_lat, country_lon, centroid['lat'], centroid['lon'])
        if distance < min_distance:
            min_distance = distance
            closest_centroid = centroid

    return closest_centroid, min_distance

# Match countries to centroids
results = []
matches_summary = []

for country in countries:
    closest_centroid, distance = find_closest_centroid(country['lat'], country['lon'], centroids)

    # Create new country entry with auto-detected position
    new_country = {
        "name": country['name'],
        "lat": closest_centroid['lat'],
        "lon": closest_centroid['lon']
    }

    # Add optional fields if they exist
    if 'population' in country:
        new_country['population'] = country['population']
    if 'capital' in country:
        new_country['capital'] = country['capital']

    results.append(new_country)

    # Track match info for summary
    matches_summary.append({
        'country': country['name'],
        'old_lat': country['lat'],
        'old_lon': country['lon'],
        'new_lat': closest_centroid['lat'],
        'new_lon': closest_centroid['lon'],
        'centroid_id': closest_centroid['id'],
        'distance': round(distance, 4),
        'centroid_area': closest_centroid['approximate_area']
    })

# Sort by distance to see potential issues
matches_summary.sort(key=lambda x: x['distance'])

# Write the output file
with open('/var/www/zemepis/data/countries_auto.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Print summary
print("=" * 100)
print("CENTROID MATCHING SUMMARY")
print("=" * 100)
print(f"{'Country':<20} {'Centroid ID':<12} {'Old Position':<20} {'New Position':<20} {'Distance':<10}")
print("-" * 100)

for match in matches_summary:
    old_pos = f"({match['old_lat']:.2f}, {match['old_lon']:.2f})"
    new_pos = f"({match['new_lat']:.2f}, {match['new_lon']:.2f})"
    print(f"{match['country']:<20} {match['centroid_id']:<12} {old_pos:<20} {new_pos:<20} {match['distance']:<10.4f}")

print("-" * 100)
print(f"\nTotal countries matched: {len(matches_summary)}")
print(f"Average distance: {sum(m['distance'] for m in matches_summary) / len(matches_summary):.4f}")
print(f"Max distance: {max(m['distance'] for m in matches_summary):.4f} ({max(matches_summary, key=lambda x: x['distance'])['country']})")
print(f"Min distance: {min(m['distance'] for m in matches_summary):.4f} ({min(matches_summary, key=lambda x: x['distance'])['country']})")
print("\n" + "=" * 100)
print(f"Output saved to: /var/www/zemepis/data/countries_auto.json")
print("=" * 100)
