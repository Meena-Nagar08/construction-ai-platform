import { useState } from "react";

// Change this to your deployed backend link after deploying (e.g. on Render)
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const FEATURES = [
  { id: "safety", label: "Site Safety Check" },
  { id: "cracks", label: "Crack Detection" },
  { id: "valuation", label: "Real Estate Valuation" },
  { id: "planning", label: "Project Planning" },
  { id: "assistant", label: "Daily Site Assistant" },
];

export default function App() {
  const [feature, setFeature] = useState("safety");
  const [text, setText] = useState("");
  const [image, setImage] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!text && !image) {
      setResult("Please type something or upload an image.");
      return;
    }
    setLoading(true);
    setResult("");

    const formData = new FormData();
    formData.append("feature", feature);
    formData.append("text", text);
    if (image) formData.append("image", image);

    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data.result || data.error || "No answer received.");
    } catch (err) {
      setResult("Could not reach the server. Is the backend running?");
    }
    setLoading(false);
  }

  return (
    <div className="page">
      <h1>Construction Intelligence Platform</h1>
      <p className="subtitle">
        Upload a site photo or type a question. The AI will help you.
      </p>

      <div className="tabs">
        {FEATURES.map((f) => (
          <button
            key={f.id}
            className={feature === f.id ? "tab active" : "tab"}
            onClick={() => setFeature(f.id)}
            type="button"
          >
            {f.label}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="card">
        <textarea
          rows="4"
          placeholder="Describe the site or ask your question..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
        />

        {image && (
          <img
            className="preview"
            src={URL.createObjectURL(image)}
            alt="preview"
          />
        )}

        <button type="submit" className="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {result && (
        <div className="card result">
          <h3>Result</h3>
          <pre>{result}</pre>
        </div>
      )}
    </div>
  );
}
