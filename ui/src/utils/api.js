// ui/src/utils/api.js
export async function fetchResults(payload) {
  try {
    const res = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: payload.query,
        radiusKm: payload.radiusKm ?? 50,   // <-- send radius
      }),
    });
    const data = await res.json();
    return {
      ok: res.ok,
      data: data.results || [],
      center: data.center || null,
      markers: data.markers || [],
    };
  } catch (e) {
    console.error("API error:", e);
    return { ok: false, data: [], center: null, markers: [] };
  }
}
