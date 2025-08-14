import React, { useEffect, useState } from "react";
import ConfidenceBadge from "./ConfidenceBadge";

export default function ResultPanel({ results }){
  const [displayed, setDisplayed] = useState([]);

  useEffect(()=>{
    setDisplayed([]);
    let i = 0;
    const id = setInterval(()=>{
      if(i < results.length){
        setDisplayed(prev=>[...prev, results[i]]);
        i++;
      } else clearInterval(id);
    }, 90); // gentle type-out
    return ()=> clearInterval(id);
  }, [results]);

  return (
    <div className="panel">
      <h3>Results</h3>
      <ul className="result-list">
        {displayed.length === 0 && <li className="result-item">No results yet.</li>}
        {displayed.map((r,idx)=>(
          <li className="result-item" key={idx}>
            <h4 className="result-title">{r.title}</h4>
            <p className="result-desc">{r.description}</p>
            <div className="badges">
              <ConfidenceBadge score={r.score ?? 0.0}/>
              {r.annotation && <span className="badge">{r.annotation}</span>}
              {r.distanceKm!=null && <span className="badge">{r.distanceKm.toFixed(2)} km</span>}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
