import { useEffect, useState } from "react";

export function Diagnostics() {
  const [status, setStatus] = useState<Record<string, any>>({});
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkEndpoints = async () => {
      try {
        const results = {
          timestamp: new Date().toISOString(),
          apiBaseUrl: import.meta.env.VITE_API_URL || "not set",
          isProd: import.meta.env.PROD,
          viteEnv: {
            MODE: import.meta.env.MODE,
            BASE_URL: import.meta.env.BASE_URL,
          },
        };

        try {
          const healthRes = await fetch("/api/healthz");
          const healthData = await healthRes.json();
          (results as any).healthz = {
            ok: healthRes.ok,
            status: healthRes.status,
            data: healthData,
          };
        } catch (e) {
          (results as any).healthz = { error: String(e) };
        }

        try {
          const summaryRes = await fetch("/api/stats/summary");
          const summaryData = await summaryRes.json();
          (results as any).summary = {
            ok: summaryRes.ok,
            status: summaryRes.status,
            data: summaryData,
          };
        } catch (e) {
          (results as any).summary = { error: String(e) };
        }

        try {
          const productsRes = await fetch("/api/products?limit=1");
          const productsData = await productsRes.json();
          (results as any).products = {
            ok: productsRes.ok,
            status: productsRes.status,
            count: Array.isArray(productsData) ? productsData.length : 0,
            data: productsData,
          };
        } catch (e) {
          (results as any).products = { error: String(e) };
        }

        try {
          const lowStockRes = await fetch("/api/stats/low-stock");
          const lowStockData = await lowStockRes.json();
          (results as any).lowStock = {
            ok: lowStockRes.ok,
            status: lowStockRes.status,
            count: Array.isArray(lowStockData) ? lowStockData.length : 0,
          };
        } catch (e) {
          (results as any).lowStock = { error: String(e) };
        }

        setStatus(results);
      } catch (e) {
        setError(String(e));
      }
    };

    checkEndpoints();
  }, []);

  return (
    <div className="p-6 bg-muted rounded-lg border border-border">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold">🔍 Diagnósticos del Sistema</h2>
        <span className="text-xs px-2 py-1 bg-background rounded">{status.timestamp?.split("T")[1]?.split(".")[0]}</span>
      </div>
      
      {error && (
        <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded text-red-600 text-sm">
          ⚠️ Error: {error}
        </div>
      )}
      
      <div className="space-y-3">
        <div className="text-xs">
          <div className="font-semibold text-foreground/70">Configuración</div>
          <ul className="text-foreground/60 space-y-1 mt-1">
            <li>🌐 API Base: <code className="bg-background px-1 rounded">{status.apiBaseUrl || "localhost:3000/api"}</code></li>
            <li>🔧 Env: <code className="bg-background px-1 rounded">{status.viteEnv?.MODE || "development"}</code></li>
            <li>📦 Base URL: <code className="bg-background px-1 rounded">{status.viteEnv?.BASE_URL || "/"}</code></li>
          </ul>
        </div>

        <div className="border-t border-border pt-3">
          <div className="font-semibold text-foreground/70 mb-2">Endpoints</div>
          <div className="grid grid-cols-2 gap-2 text-xs">
            {[
              { label: "Healthz", key: "healthz" },
              { label: "Summary", key: "summary" },
              { label: "Products", key: "products" },
              { label: "Low Stock", key: "lowStock" },
            ].map(({ label, key }) => {
              const endpoint = status[key as keyof typeof status] || {};
              const ok = (endpoint as any).ok || (endpoint as any).status === 200;
              const icon = ok ? "✅" : "❌";
              return (
                <div key={key} className="bg-background/50 p-2 rounded">
                  <div>{icon} {label}</div>
                  <div className="text-foreground/50 text-[10px] mt-1">
                    {ok ? `Status ${(endpoint as any).status}` : `Error: ${(endpoint as any).error || "unknown"}`}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <details className="border-t border-border pt-3 text-xs">
          <summary className="cursor-pointer font-semibold text-foreground/70 hover:text-foreground">
            📊 Datos Completos
          </summary>
          <pre className="bg-background p-3 rounded mt-2 overflow-auto max-h-64 text-[11px]">
            {JSON.stringify(status, null, 2)}
          </pre>
        </details>
      </div>
    </div>
  );
}
