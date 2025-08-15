# src/server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict
from pathlib import Path
import math
import random
import re
import time
import logging
from datetime import date

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Geo-RAG API (Demo Mode)", version="1.0")

# Allow the React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve /static from data/ folder
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
app.mount("/static", StaticFiles(directory=str(DATA_DIR)), name="static")

# --------- Models ---------
class QueryIn(BaseModel):
    query: str
    radiusKm: Optional[float] = 50.0

# --------- Helpers ---------
def _maybe_satellite_url(title: str) -> Optional[str]:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"/static/satellite/{slug}.png"

def _haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlmb/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def _fake_geo_results(query: str, radius_km: float) -> List[Dict]:
    """Generate 100% fake but realistic and query-matching results."""
    logging.info(f"🔍 Processing query: '{query}'")
    time.sleep(random.uniform(0.2, 0.4))  # faster but still human-like

    # Always fix center to a plausible Delhi coordinate if query mentions it
    if "delhi" in query.lower():
        center_lat, center_lon = 28.6139, 77.2090
    else:
        center_lat = round(random.uniform(-60, 60), 5)
        center_lon = round(random.uniform(-150, 150), 5)

    results = []
    for i in range(8):  # fixed number for cleaner UI
        lat = center_lat + random.uniform(-0.05, 0.05)
        lon = center_lon + random.uniform(-0.05, 0.05)
        dist = _haversine_km(center_lat, center_lon, lat, lon)

        results.append({
            "title": f"{query.title()} — Report {i+1}",
            "description": f"Detailed geospatial analysis for '{query}' generated on {date.today().strftime('%d %B %Y')}.",
            "score": round(random.uniform(0.88, 0.99), 3),  # high confidence
            "annotation": f"✅ Within {int(radius_km)} km",  # always inside range
            "satellite": _maybe_satellite_url(f"{query}-report-{i+1}"),
            "distance_km": round(dist, 2),
            "geo_type": "river" if "river" in query.lower() else "landmark"
        })

    logging.info(f"✅ Generated {len(results)} fake realistic results.")
    return {
        "center": {"lat": center_lat, "lon": center_lon, "label": query.title()},
        "markers": [
            {"lat": r["distance_km"], "lon": r["distance_km"], "label": r["title"], "type": r["geo_type"]}
            for r in results
        ],
        "results": sorted(results, key=lambda r: -r["score"])
    }

# --------- API ---------
@app.get("/health")
def health():
    return {"status": "ok", "mode": "demo"}

@app.post("/api/query")
def api_query(payload: QueryIn):
    q = payload.query.strip()
    radius_km = float(payload.radiusKm or 50.0)
    if not q:
        return {"query": q, "results": [], "center": None, "markers": []}
    fake_data = _fake_geo_results(q, radius_km)
    return {
        "query": q,
        "center": fake_data["center"],
        "markers": fake_data["markers"],
        "results": fake_data["results"]
    }
