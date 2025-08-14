import React, { useState } from "react";

const TABS = ["General", "Land Use", "Climate & Weather", "Population", "Infrastructure"];

export default function QueryPanel({ onSearch, loading }){
  const [active, setActive] = useState("General");
  const [query, setQuery] = useState("");
  const [radius, setRadius] = useState(10);

  const submit = (e)=>{
    e.preventDefault();
    if(!query.trim()) return;
    onSearch({ query, type: active, radiusKm: Number(radius) });
  };

  return (
    <div className="panel">
      <h3>Spatial Query Interface</h3>

      <div className="controls" role="tablist" aria-label="Query Type">
        {TABS.map(t => (
          <button
            key={t}
            className={`pill ${active===t?'active':''}`}
            onClick={()=>setActive(t)}
            type="button"
          >
            {t}
          </button>
        ))}
      </div>

      <form onSubmit={submit}>
        <div className="query-bar">
          <input
            className="query-input"
            placeholder='Ask about a location… e.g., "Nearest river to 28.61, 77.21"'
            value={query}
            onChange={e=>setQuery(e.target.value)}
          />
          <button className="query-btn" disabled={loading}>
            {loading ? "Analyzing…" : "Analyze Location"}
          </button>
        </div>

        <div className="meta-row">
          <label>Search Radius (km)</label>
          <input
            type="number"
            min="1"
            step="1"
            value={radius}
            onChange={e=>setRadius(e.target.value)}
          />
        </div>
      </form>
    </div>
  );
}
