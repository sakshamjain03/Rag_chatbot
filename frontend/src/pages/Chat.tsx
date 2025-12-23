import { useEffect, useState } from "react";
import { api } from "../api/client";
import AppLayout from "../layout/AppLayout";

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

  async function ask() {
    const res = await api.post("/", { query });
    setAnswer(res.data.answer);
  }

  return (
    <AppLayout>
      <div className="max-w-4xl mx-auto space-y-6">
        <h2 className="text-2xl font-semibold">Chat with your files</h2>

        {/* Upload */}
        <div className="bg-white p-4 rounded shadow">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
          <button
            onClick={upload}
            className="ml-2 bg-blue-600 text-white px-4 py-1 rounded"
          >
            Upload
          </button>
        </div>

        {/* Assets */}
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-semibold mb-2">Your Assets</h3>
          <ul className="text-sm">
            {assets.map((a) => (
              <li key={a.id} className="border-b py-1">
                {a.original_name} ({a.asset_type})
              </li>
            ))}
          </ul>
        </div>

        {/* Chat */}
        <div className="bg-white p-4 rounded shadow space-y-2">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about your files..."
            className="w-full border p-2 rounded"
          />
          <button
            onClick={ask}
            className="bg-green-600 text-white px-4 py-1 rounded"
          >
            Ask
          </button>

          {answer && (
            <div className="mt-3 p-3 bg-gray-50 border rounded">
              {answer}
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
