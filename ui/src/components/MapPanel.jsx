import React, { useMemo } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix default marker icons in CRA
import marker2x from "leaflet/dist/images/marker-icon-2x.png";
import marker from "leaflet/dist/images/marker-icon.png";
import shadow from "leaflet/dist/images/marker-shadow.png";
const DefaultIcon = L.icon({ iconUrl: marker, iconRetinaUrl: marker2x, shadowUrl: shadow });
L.Marker.prototype.options.icon = DefaultIcon;

export default function MapPanel({ center, markers = [] }) {
  const mapCenter = useMemo(
    () => (center ? [center.lat, center.lon] : [20, 0]), // default world view
    [center]
  );

  const zoom = center ? 7 : 2;

  return (
    <div className="panel">
      <h3>Map</h3>
      <div className="map-wrap">
        <MapContainer center={mapCenter} zoom={zoom} scrollWheelZoom={true} style={{ height: "100%", width: "100%" }}>
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {markers.map((m, idx) => (
            <Marker key={idx} position={[m.lat, m.lon]}>
              <Popup>
                <b>{m.label}</b><br/>
                <small>{m.type}</small>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
