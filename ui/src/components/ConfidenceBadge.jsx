import React from "react";

export default function ConfidenceBadge({ score }){
  const pct = Math.round(score*100);
  let cls = "silver";
  if (pct >= 85) cls = "gold";
  else if (pct >= 65) cls = "cyan";
  return <span className={`badge ${cls}`}>Confidence {pct}%</span>;
}
