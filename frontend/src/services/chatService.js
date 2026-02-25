const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function sendQuestion(question, filters = {}) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // CORRECCIÓN: Usamos '...filters' para aplanar el objeto
    // Genera: { "question": "...", "sistema": "...", "marca": "..." }
    body: JSON.stringify({ question, ...filters }), 
  });

  if (!response.ok) throw new Error("Error con la solicitud al servicio de IA");
  return response.json();
}