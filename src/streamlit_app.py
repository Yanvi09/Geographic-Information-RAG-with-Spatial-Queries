# src/streamlit_app.py
import time, math, re
from pathlib import Path

import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
import folium
from streamlit.components.v1 import html

st.set_page_config(page_title="GeoRAG Spatial Demo", page_icon="🌍", layout="wide")

# ---------- Helpers ----------
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dlmb/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def find_name_in_query(q, series):
    ql = q.lower()
    for n in series:
        if str(n).lower() in ql:
            return str(n)
    return None

def repr_latlon(geom):
    pt = geom.representative_point()
    return float(pt.y), float(pt.x)

@st.cache_resource(show_spinner=False)
def load_data():
    base = Path(__file__).resolve().parents[1] / "data"
    cities = gpd.read_file(base / "cities.geojson")
    rivers = gpd.read_file(base / "rivers.geojson")
    return base, cities, rivers

# ---------- UI ----------
st.title("🌍 Geographic Information RAG — Spatial Query Demo")
st.caption("Demo mode: semantic + spatial filtering over sample GeoJSON (no external APIs).")

base_dir, cities_gdf, rivers_gdf = load_data()

colL, colR = st.columns([1,1])
with colL:
    q = st.text_input("Ask a spatial question", value="nearest river in delhi")
with colR:
    radius_km = st.slider("Search radius (km)", 5, 200, 25)

btn = st.button("Run")

# ---------- Core ----------
if btn or q.strip():
    t0 = time.time()

    city_in_q  = find_name_in_query(q, cities_gdf["name"])
    river_in_q = find_name_in_query(q, rivers_gdf["name"])

    # 1) Decide a center
    center = None
    if city_in_q:
        row = cities_gdf[cities_gdf["name"] == city_in_q].iloc[0]
        clat, clon = repr_latlon(row.geometry)
        center = (clat, clon, f"{city_in_q} (city)")
    elif river_in_q:
        row = rivers_gdf[rivers_gdf["name"] == river_in_q].iloc[0]
        clat, clon = repr_latlon(row.geometry)
        center = (clat, clon, f"{river_in_q} (river)")

    # fallback if nothing detected
    if center is None:
        # pick the first city as a neutral center
        row = cities_gdf.iloc[0]
        clat, clon = repr_latlon(row.geometry)
        center = (clat, clon, f"{row['name']} (auto)")

    # 2) Choose target layer based on query intent
    target = rivers_gdf if ("river" in q.lower() or "nearest river" in q.lower()) else cities_gdf

    # 3) Compute distances & filter by radius
    results = []
    for _, r in target.iterrows():
        lat, lon = repr_latlon(r.geometry)
        d = haversine_km(center[0], center[1], lat, lon)
        if d <= radius_km:
            results.append({
                "title": r.get("name", "Unknown"),
                "distance_km": round(d, 2),
                "type": "river" if target is rivers_gdf else "city"
            })

    # If none within radius, show the nearest 5 with a warning
    if not results:
        # compute all, take 5 closest
        tmp = []
        for _, r in target.iterrows():
            lat, lon = repr_latlon(r.geometry)
            d = haversine_km(center[0], center[1], lat, lon)
            tmp.append({
                "title": r.get("name", "Unknown"),
                "distance_km": round(d, 2),
                "type": "river" if target is rivers_gdf else "city"
            })
        tmp.sort(key=lambda x: x["distance_km"])
        results = tmp[:5]
        st.warning(f"No features within {radius_km} km. Showing nearest {len(results)}.")

    # 4) Map
    m = folium.Map(location=[center[0], center[1]], zoom_start=9, tiles="OpenStreetMap")
    folium.Marker([center[0], center[1]], tooltip=f"Center: {center[2]}", icon=folium.Icon(color="red")).add_to(m)
    for r in results:
        # locate feature geometry again to plot
        gdf = rivers_gdf if r["type"] == "river" else cities_gdf
        row = gdf[gdf["name"] == r["title"]].iloc[0]
        lat, lon = repr_latlon(row.geometry)
        folium.CircleMarker(
            location=[lat, lon],
            radius=6,
            tooltip=f"{r['title']} • {r['type']} • {r['distance_km']} km",
            fill=True
        ).add_to(m)

    html(m.get_root().render(), height=520)

    # 5) Results + metric
    with st.expander("Results", expanded=True):
        for i, r in enumerate(sorted(results, key=lambda x: x["distance_km"])):
            st.write(f"**{i+1}. {r['title']}** — {r['type']} • {r['distance_km']} km")

    st.caption(f"⏱ Query time: {time.time() - t0:.2f}s • Radius: {radius_km} km • Query: “{q}”")

