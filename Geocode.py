import pandas as pd
from geopy.geocoders import OpenCage
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import folium
file_path = 

# Load the dataset
df = pd.read_csv(file_path)


geolocator = OpenCage(api_key='your API key (sign up at https://opencagedata.com/)')



# Function to clean addresses by removing parentheses
def clean_address(address):
    if pd.isna(address):
        return address
    # Remove parentheses and their contents
    address = address.split('(')[0].strip()
    return address

# Function to geocode an address with rate limiting
def geocode_address(address, max_retries=3, delay=2):
    if pd.isna(address):  # Skip NaN values
        return (None, None)

    print(f"Processing address: {address}")  

    # Clean the address by removing parentheses
    address = clean_address(address)

    for attempt in range(max_retries):
        try:
            # Handle street segments (must contain both FROM and TO)
            if 'FROM' in address and 'TO' in address:
                print(f"Handling street segment: {address}")  # Debugging print statement
                parts = address.split('FROM')
                street = parts[0].replace('ON', '').strip()
                start_end = parts[1].split('TO')
                if len(start_end) == 2:  # Ensure the address contains both start and end
                    start = start_end[0].strip()
                    end = start_end[1].strip()

                    # Geocode the start and end points
                    print(f"Geocoding start: {start} {street}, Chicago, IL")  # Debugging print statement
                    start_location = geolocator.geocode(f"{start} {street}, Chicago, IL", timeout=10)
                    print(f"Geocoding end: {end} {street}, Chicago, IL")  # Debugging print statement
                    end_location = geolocator.geocode(f"{end} {street}, Chicago, IL", timeout=10)

                    if start_location and end_location:
                        # Calculate the midpoint of the segment
                        midpoint = (
                            (start_location.latitude + end_location.latitude) / 2,
                            (start_location.longitude + end_location.longitude) / 2
                        )
                        return midpoint
                    else:
                        return (41.8781, -87.6298)  # Default to Chicago's center
                else:
                    # If the address doesn't contain both start and end, treat it as a single place
                    print(f"Invalid street segment format: {address}. Treating as single place.")
                    location = geolocator.geocode(address + ", Chicago, IL", timeout=10)
                    return (location.latitude, location.longitude) if location else (41.8781, -87.6298)

            # Handle intersections
            elif '&' in address:
                print(f"Handling intersection: {address}")  # Debugging print statement
                parts = address.split('&')
                if len(parts) >= 2:  # Ensure there are at least two parts
                    part1 = parts[0].strip() + ", Chicago, IL"
                    part2 = parts[1].strip() + ", Chicago, IL"

                    # Geocode both parts of the intersection
                    print(f"Geocoding part 1: {part1}")  # Debugging print statement
                    loc1 = geolocator.geocode(part1, timeout=10)
                    print(f"Geocoding part 2: {part2}")  # Debugging print statement
                    loc2 = geolocator.geocode(part2, timeout=10)

                    if loc1 and loc2:
                        # Calculate the midpoint of the intersection
                        midpoint = (
                            (loc1.latitude + loc2.latitude) / 2,
                            (loc1.longitude + loc2.longitude) / 2
                        )
                        return midpoint
                    else:
                        return (41.8781, -87.6298)  # Default to Chicago's center
                else:
                    # If the address doesn't contain two parts, treat it as a single place
                    print(f"Invalid intersection format: {address}. Treating as single place.")
                    location = geolocator.geocode(address + ", Chicago, IL", timeout=10)
                    return (location.latitude, location.longitude) if location else (41.8781, -87.6298)

            # Handle single places
            else:
                print(f"Handling single place: {address}")  # Debugging print statement
                location = geolocator.geocode(address + ", Chicago, IL", timeout=10)
                return (location.latitude, location.longitude) if location else (41.8781, -87.6298)  # Default to Chicago's center

        except GeocoderTimedOut:
            print(f"Attempt {attempt + 1} failed for {address}. Retrying...")
            time.sleep(delay)  # Wait before retrying
        except GeocoderServiceError as e:
            print(f"Geocoding service error for {address}: {e}")
            return (None, None)
        except Exception as e:
            print(f"Error geocoding {address}: {e}")
            return (None, None)

    print(f"Max retries reached for {address}. Skipping...")
    return (None, None)

# Load the full dataset
file_path = r""  # Replace with your actual file path
df = pd.read_csv(file_path)

# Check if a checkpoint file exists to resume from
checkpoint_file = r""  # Replace with your desired checkpoint file path
try:
    df_geocoded = pd.read_csv(checkpoint_file)
    print("Resuming from checkpoint...")
except FileNotFoundError:
    df_geocoded = df.copy()
    df_geocoded['coordinates'] = None
    df_geocoded['latitude'] = None
    df_geocoded['longitude'] = None
    print("Starting from the beginning...")

# Geocode addresses in batches
batch_size = 1000  # Number of addresses to process in one batch
delay_between_requests = 0.07  # Delay to stay within 15 requests/sec (1/15 ≈ 0.067)

for i in range(0, len(df_geocoded), batch_size):
    print(f"Processing batch {i//batch_size + 1}...")
    batch = df_geocoded.iloc[i:i + batch_size]

    for index, row in batch.iterrows():
        if pd.isna(row['coordinates']):  # Skip already geocoded addresses
            coordinates = geocode_address(row['description'])
            df_geocoded.at[index, 'coordinates'] = str(coordinates)
            df_geocoded.at[index, 'latitude'] = coordinates[0] if coordinates else None
            df_geocoded.at[index, 'longitude'] = coordinates[1] if coordinates else None
            time.sleep(delay_between_requests)  # Respect the rate limit

    # Save progress to the checkpoint file
    df_geocoded.to_csv(checkpoint_file, index=False)
    print(f"Checkpoint saved after processing {i + batch_size} addresses.")

# Save the fully geocoded dataset
output_file_path = r""  # Replace with your desired output path
df_geocoded.to_csv(output_file_path, index=False)

print("Geocoding complete! File saved to:", output_file_path)

# Create a map centered on Chicago
chicago_map = folium.Map(location=[41.8781, -87.6298], zoom_start=12)

# Create FeatureGroups for each year and ward combination
year_ward_groups = {}

# Iterate through the dataset and add markers to the appropriate FeatureGroup
for index, row in df_geocoded.iterrows():
    if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
        # Create a unique key for the year and ward combination
        key = f"Year {row['year']} - Ward {row['ward']}"
        
        # Create a FeatureGroup if it doesn't already exist
        if key not in year_ward_groups:
            year_ward_groups[key] = folium.FeatureGroup(name=key)
        
        # Create the popup content with ward, year, category, and program
        popup_content = f"""
        <b>Address:</b> {row['description']}<br>
        <b>Ward:</b> {row['ward']}<br>
        <b>Year:</b> {row['year']}<br>
        <b>Category:</b> {row['category']}<br>
        <b>Program:</b> {row['program']}<br>
        <b>Cost:</b> ${row['cost']}
        """
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_content, max_width=300),  # Set max width for better readability
        ).add_to(year_ward_groups[key])

# Add all FeatureGroups to the map
for group in year_ward_groups.values():
    group.add_to(chicago_map)

# Add a LayerControl to toggle year and ward groups
folium.LayerControl().add_to(chicago_map)

# Save the map to an HTML file
map_output_path = r"C:\Users\17049\OneDrive\Documents\R\chicago_geocoded_map.html"  # Replace with your desired output path
chicago_map.save(map_output_path)

print("Map with toggle menu created and saved to:", map_output_path)
