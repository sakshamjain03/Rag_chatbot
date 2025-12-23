import { useEffect, useState } from "react";
import { api } from "../api/client";

interface Asset {
  id: string;
  original_name: string;
  asset_type: string;
}

export default function AssetList() {
  const [assets, setAssets] = useState<Asset[]>([]);

  useEffect(() => {
    api.get("/assets/").then((res) => setAssets(res.data));
  }, []);

  return (
    <div>
      <h3>Your Assets</h3>
      {assets.map((a) => (
        <div key={a.id}>
          {a.asset_type === "image" ? "🖼️" : "📄"} {a.original_name}
        </div>
      ))}
    </div>
  );
}
