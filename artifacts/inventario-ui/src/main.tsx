import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css";

// Enhanced debugging for dev mode
if (import.meta.env.DEV) {
  console.log("🚀 App initialized in DEV mode");
  console.log("📍 Environment:", {
    VITE_API_URL: import.meta.env.VITE_API_URL,
    MODE: import.meta.env.MODE,
    BASE_URL: import.meta.env.BASE_URL,
    PROD: import.meta.env.PROD,
  });

  const originalError = console.error;
  console.error = function(...args: any[]) {
    originalError.apply(console, args);
  };

  window.addEventListener("unhandledrejection", (event) => {
    console.error("🔴 Unhandled rejection:", event.reason);
  });

  window.addEventListener("error", (event) => {
    console.error("🔴 Global error:", event.error);
    console.error("Stack:", event.error?.stack);
  });
}

const root = document.getElementById("root");
if (!root) {
  const errorMsg = "Root element not found - check index.html for <div id=\"root\"></div>";
  console.error("🔴", errorMsg);
  throw new Error(errorMsg);
}

console.log("✅ Root element found, rendering App...");

try {
  createRoot(root).render(<App />);
  console.log("✅ App rendered successfully");
} catch (error) {
  console.error("🔴 Error rendering app:", error);
  root.innerHTML = `<div style="padding: 20px; color: red; font-family: monospace;">
    <h1>Error renderizando la aplicación</h1>
    <pre>${String(error)}</pre>
  </div>`;
}
