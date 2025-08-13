import geopandas as gpd
from PIL import Image
import os
import json

# ===== Step 1: Load GIS Data =====
rivers = gpd.read_file("data/rivers.geojson")
print("Rivers data preview:")
print(rivers.head())

cities = gpd.read_file("data/cities.geojson")
print("Cities data preview:")
print(cities.head())

# ===== Step 2: Load and Preprocess Satellite Images =====
satellite_dir = "data/satellite/"
sat_images = {}

for file in os.listdir(satellite_dir):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        path = os.path.join(satellite_dir, file)
        img = Image.open(path).resize((256, 256))  # resize for embedding
        sat_images[file.split(".")[0]] = img

print("Satellite images loaded:", list(sat_images.keys()))

# ===== Step 3: Load Textual Info =====
text_info_path = "data/textual_info.json"
with open(text_info_path, "r", encoding="utf-8") as f:
    text_info = json.load(f)

print("Textual info loaded:", list(text_info.keys()))
