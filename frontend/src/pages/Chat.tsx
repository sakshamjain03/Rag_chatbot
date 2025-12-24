import { useEffect, useState } from "react";
import { api } from "../api/client";
import "../styles/chat.css";

export default function Chat() {
  const [file, setFile] = useState<File | null>(null);
  const [assets, setAssets] = useState<any[]>([]);
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");

  async function loadAssets() {
    const res = await api.get("/assets/");
    setAssets(res.data);
  }

  useEffect(() => {
    loadAssets();
  }, []);

  async function upload() {
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    await api.post("/assets/upload/", form);
    setFile(null);
    loadAssets();
  }

  async function deleteAsset(id: string) {
    await api.delete(`/assets/${id}/`);
    loadAssets();
  }

  async function ask() {
    const res = await api.post("/", { query });
    setAnswer(res.data.answer);
  }

  return (
    <div className="chat-container">
      <div className="chat-card">
        <h2>Chat with your files</h2>

        <div className="file-row">
          <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
          <button onClick={upload}>Upload</button>
        </div>
      </div>

      <div className="chat-card assets-box">
        <h3>Your Assets</h3>

        {assets.map((a) => (
          <div key={a.id} className="asset-row">
            <div>
              <strong>{a.original_name}</strong>
              <div className="meta">
                {a.asset_type.toUpperCase()} · {(a.size_bytes / 1024).toFixed(1)} KB ·{" "}
                {new Date(a.uploaded_at).toLocaleString()}
              </div>
            </div>

            <button className="delete-btn" onClick={() => deleteAsset(a.id)}>
              🗑
            </button>
          </div>
        ))}
      </div>

      <div className="chat-card">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about your files..."
        />

        <button className="ask-btn" onClick={ask}>
          Ask
        </button>

        {answer && <div className="answer-box">{answer}</div>}
      </div>
    </div>
  );
}
