import React from "react";

export default function Header(){
  return (
    <div className="header">
      <div className="brand-mark">AI</div>
      <div className="title-wrap">
        <h1>GeoRAG Intelligence Demo</h1>
        <div className="sub">Geographic Information Retrieval & Spatial Analysis</div>
      </div>

      <div className="kpis">
        <div className="kpi"><span className="dot"></span>System Ready</div>
        <div className="kpi">Live Data</div>
      </div>
    </div>
  );
}
