import React from "react";

const features = [
  { title: "Satellite Analysis", text: "Multi-spectral imagery processing" },
  { title: "Spatial Indexing", text: "Geographic data retrieval" },
  { title: "AI Processing", text: "Natural language queries" },
  { title: "Precision Results", text: "Location-specific insights" }
];

export default function FeatureCards(){
  return (
    <div className="features">
      {features.map((f,i)=>(
        <div className="feature-card" key={i}>
          <h4>{f.title}</h4>
          <p>{f.text}</p>
        </div>
      ))}
    </div>
  );
}
