import React, { useEffect, useState } from "react";
import ConfidenceBadge from "./ConfidenceBadge";

export default function ResultPanel({ results }) {
  const safeResults = Array.isArray(results) ? results : [];
  const [displayed, setDisplayed] = useState([]);

  useEffect(() => {
    setDisplayed([]);
    let i = 0;
    const id = setInterval(() => {
      if (i < safeResults.length) {
        setDisplayed((prev) => [...prev, safeResults[i]]);
        i++;
      } else {
        clearInterval(id);
      }
    }, 90); // gentle type-out
    return () => clearInterval(id);
  }, [safeResults]);

  return (
    <div className="panel">
      <h3>Results</h3>
      <ul className="result-list">
        {displayed.length === 0 && (
          <li className="result-item">No results yet.</li>
        )}
        {displayed.map((r, idx) => {
          if (!r) return null; // skip undefined entries
          return (
            <li className="result-item" key={idx}>
              <h4 className="result-title">{r.title ?? "Untitled"}</h4>
              <p className="result-desc">{r.description ?? ""}</p>
              <div className="badges">
                <ConfidenceBadge score={r.score ?? 0.0} />
                {r.annotation && <span className="badge">{r.annotation}</span>}
                {typeof r.distanceKm === "number" && (
                  <span className="badge">
                    {r.distanceKm.toFixed(2)} km
                  </span>
                )}
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
