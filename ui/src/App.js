import React, { useState } from "react";
import "./styles.css";

import Header from "./components/Header";
import FeatureCards from "./components/FeatureCards";
import QueryPanel from "./components/QueryPanel";
import ResultPanel from "./components/ResultPanel";
import MapPanel from "./components/MapPanel";

import { fetchResults } from "./utils/api";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [center, setCenter] = useState(null);

  const handleSearch = async (payload) => {
    setLoading(true);
    try {
      const res = await fetchResults(payload); // mocked for now
      if (res.ok) {
        setResults(res.data);
        setCenter(res.center);
      } else {
        setResults([]);
        setCenter(null);
      }
    } catch (e) {
      console.error(e);
      setResults([]);
      setCenter(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <Header />

      <div className="hero">
        <h2>Geographic Intelligence</h2>
        <p>
          Combine satellite imagery, geographic databases, and AI to analyze
          spatial relationships and extract location-based insights.
        </p>
        <FeatureCards />
      </div>

      <div className="main">
        <MapPanel results={results} center={center} />
        <div className="right">
          <QueryPanel onSearch={handleSearch} loading={loading} />
          <div style={{ height: 12 }} />
          <ResultPanel results={results} />
        </div>
      </div>

      <div className="footer">
        Built with Curosity—{" "}
        <b style={{ color: "var(--gold)" }}>Powered By</b> Anvi Yadav - CS Major 
      </div>
    </div>
  );
}
