import React, { useState } from "react";
import "./styles.css";

import Header from "./components/Header";
import FeatureCards from "./components/FeatureCards";
import QueryPanel from "./components/QueryPanel";
import ResultPanel from "./components/ResultPanel";
import MapPanel from "./components/MapPanel";

import { fetchResults } from "./utils/api";

export default function App(){
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [center, setCenter] = useState(null);
  const [markers, setMarkers] = useState([]);

  const handleSearch = async (payload)=>{
    setLoading(true);
    const res = await fetchResults(payload);
    if(res.ok){
      setResults(res.data);
      setCenter(res.center);
      setMarkers(res.markers);
    } else {
      setResults([]);
      setCenter(null);
      setMarkers([]);
    }
    setLoading(false);
  };

  return (
    <div className="page">
      <Header/>

      <div className="hero">
        <h2>AI-Powered Geographic Intelligence</h2>
        <p>
          Combine satellite imagery, geographic databases, and AI to analyze spatial relationships
          and extract location-based insights.
        </p>
        <FeatureCards/>
      </div>

      <div className="main">
        <MapPanel results={results} center={center} markers={markers}/>
        <div className="right">
          <QueryPanel onSearch={handleSearch} loading={loading}/>
          <div style={{height:12}}/>
          <ResultPanel results={results}/>
        </div>
      </div>

      <div className="footer">
        Built by Curosity — <b style={{color:"var(--gold)"}}></b> Powered By: Anvi Yadav-CS Major.
      </div>
    </div>
  );
}
