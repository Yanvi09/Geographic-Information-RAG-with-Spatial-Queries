# src/spatial_queries.py
import geopandas as gpd
from shapely.geometry import Point, box
from rtree import index

# Load GIS datasets
cities_gdf = gpd.read_file("data/cities.geojson")
rivers_gdf = gpd.read_file("data/rivers.geojson")

# Build spatial indexes for fast nearest neighbor
cities_idx = index.Index()
for idx, geom in enumerate(cities_gdf.geometry):
    cities_idx.insert(idx, geom.bounds)

rivers_idx = index.Index()
for idx, geom in enumerate(rivers_gdf.geometry):
    rivers_idx.insert(idx, geom.bounds)

# ------------------ Core Functions ------------------ #

def point_in_polygon(lat, lon, gdf, buffer=0.0):
    """Return list of features containing the point (with optional small buffer)."""
    pt = Point(lon, lat).buffer(buffer)
    matches = gdf[gdf.geometry.intersects(pt)]
    return matches["name"].tolist() if "name" in gdf else matches["id"].tolist()


def nearest_feature(lat, lon, gdf, idx):
    """Return nearest feature and distance from point."""
    pt = Point(lon, lat)
    nearest = None
    min_dist = float("inf")
    # Use rtree to reduce candidates
    for candidate_idx in list(idx.nearest(pt.bounds, 5)):
        geom = gdf.geometry.iloc[candidate_idx]
        dist = pt.distance(geom)
        if dist < min_dist:
            min_dist = dist
            nearest = gdf.iloc[candidate_idx]
    if nearest is not None:
        return nearest["name"] if "name" in nearest else nearest["id"], min_dist
    return None, None


def features_in_bbox(min_lat, min_lon, max_lat, max_lon, gdf):
    """Return features intersecting a bounding box."""
    bbox = box(min_lon, min_lat, max_lon, max_lat)
    matches = gdf[gdf.geometry.intersects(bbox)]
    return matches["name"].tolist() if "name" in gdf else matches["id"].tolist()


# ------------------ Xiao Nai-style Tests ------------------ #
if __name__ == "__main__":
    print(">> Test 1: Point in polygon (should match a city):")
    cities_found = point_in_polygon(28.6139, 77.2090, cities_gdf, buffer=0.01)
    print(cities_found)

    print("\n>> Test 2: Nearest river to a point:")
    nearest_river, dist = nearest_feature(28.6139, 77.2090, rivers_gdf, rivers_idx)
    print(nearest_river, dist)

    print("\n>> Test 3: Features in bounding box:")
    bbox_features = features_in_bbox(28.5, 77.0, 28.7, 77.3, cities_gdf)
    print(bbox_features)
