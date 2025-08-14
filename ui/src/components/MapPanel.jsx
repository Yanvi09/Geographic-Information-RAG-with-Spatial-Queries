import React, { useEffect, useMemo } from "react";
import { MapContainer, TileLayer, Marker, Rectangle, Popup, useMap } from "react-leaflet";
import L from "leaflet";

const markerIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25,41], iconAnchor: [12,41], popupAnchor: [1,-34], shadowSize: [41,41]
});

function FitToContent({ results, center }){
  const map = useMap();
  useEffect(()=>{
    const bounds = [];
    if (center) bounds.push([center.lat, center.lon]);
    results.forEach(r=>{
      if(r.coords) bounds.push([r.coords.lat, r.coords.lon]);
      if(r.bbox){
        const [w,s,e,n] = r.bbox;
        bounds.push([s,w]); bounds.push([n,e]);
      }
    });
    if(bounds.length>0) map.fitBounds(bounds, { padding:[18,18] });
  }, [results, center, map]);
  return null;
}

export default function MapPanel({ results, center }){
  const rects = useMemo(()=> results
    .filter(r=>Array.isArray(r.bbox))
    .map((r, i) => ({ id:i, bounds:[[r.bbox[1], r.bbox[0]], [r.bbox[3], r.bbox[2]]] })), [results]);

  return (
    <div className="panel">
      <h3>Interactive Satellite Map</h3>
      <div className="map-wrap">
        <MapContainer center={[28.6139, 77.209]} zoom={11} scrollWheelZoom={true}>
          <TileLayer
            attribution='&copy; OpenStreetMap, &copy; CARTO'
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          />
          {center && (
            <Marker position={[center.lat, center.lon]} icon={markerIcon}>
              <Popup>Query Point</Popup>
            </Marker>
          )}
          {results.filter(r=>r.coords).map((r, i)=>(
            <Marker key={i} position={[r.coords.lat, r.coords.lon]} icon={markerIcon}>
              <Popup>{r.title}</Popup>
            </Marker>
          ))}
          {rects.map(r=> <Rectangle key={r.id} bounds={r.bounds} pathOptions={{color:"#9ad8f1"}} />)}
          <FitToContent results={results} center={center}/>
        </MapContainer>
      </div>
    </div>
  );
}
