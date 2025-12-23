import { useState } from "react";
import { api } from "../api/client";

interface Source {
  asset: string;
  snippet: string;
}

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<any[]>([]);

  const send = async () => {
    if (!query.trim()) return;

    const userMsg = { role: "user", content: query };
    setMessages((m) => [...m, userMsg]);

    const res = await api.post("/chat/", { query });

    setMessages((m) => [
      ...m,
      {
        role: "assistant",
        content: res.data.answer,
        sources: res.data.sources,
      },
    ]);

    setQuery("");
  };

  return (
    <div>
      <h3>Chat</h3>

      <div style={{ minHeight: 300 }}>
        {messages.map((m, i) => (
          <div key={i}>
            <strong>{m.role}:</strong> {m.content}
            {m.sources && (
              <ul>
                {m.sources.map((s: Source, idx: number) => (
                  <li key={idx}>
                    {s.asset}: {s.snippet}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask about your files..."
      />
      <button onClick={send}>Send</button>
    </div>
  );
}
