// Mock API — returns plausible spatial RAG results for UI demo.
// Later, we will replace fetchMock with a real POST to your Python service.

export async function fetchResults({ query, type, radiusKm }){
  // tiny delay for Xiao Nai "thinking"
  await new Promise(res=>setTimeout(res, 600));

  // heuristic: if query mentions Delhi
  const isDelhi = /delhi|28\.6|77\./i.test(query);

  const demo = isDelhi ? [
    {
      title: "Nearest River: Yamuna",
      description: "The Yamuna flows along Delhi; typical distance from CP ≈ 3–6 km.",
      annotation: "✅ Near Delhi",
      score: 0.92,
      distanceKm: 3.2,
      coords: { lat: 28.6139, lon: 77.2300 },
      bbox: [77.10, 28.55, 77.32, 28.77]
    },
    {
      title: "Administrative Region: New Delhi",
      description: "Capital district; dense urban core with mixed land-use.",
      annotation: "Admin polygon matched",
      score: 0.88,
      coords: { lat: 28.61, lon: 77.21 }
    },
    {
      title: "Transport: Ring Road",
      description: "Primary arterial road forming a loop around the city.",
      annotation: "Proximity: within radius",
      score: 0.81
    }
  ] : [
    {
      title: "Topographic Hint",
      description: "Try adding coordinates, e.g., 'nearest river to 28.61, 77.21'.",
      annotation: "Tip",
      score: 0.50
    }
  ];

  return { ok:true, data: demo, center: isDelhi ? { lat:28.6139, lon:77.2090 } : null };
}
