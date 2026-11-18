
const API_URL = "http://127.0.0.1:8000";

export async function analyzeCode(code, language) {
  const response = await fetch(`${API_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      code,
      language
    })
  });

  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error("The backend returned an invalid response.");
  }

  if (!response.ok) {
    throw new Error(data.detail || "Code analysis failed.");
  }

  return data;
}
