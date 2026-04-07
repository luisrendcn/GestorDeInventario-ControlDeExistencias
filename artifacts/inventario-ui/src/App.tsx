import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Router, useLocation } from "wouter";
import { setBaseUrl } from "@workspace/api-client-react";

// Configure API - Use direct URL to API server
const apiUrl = typeof window !== "undefined" && window.location.hostname === "localhost"
  ? "http://localhost:3000/api"
  : "/api";

setBaseUrl(apiUrl);

// Import components & pages
import { Sidebar } from "@/components/layout/Sidebar";
import Dashboard from "@/pages/Dashboard";
import Products from "@/pages/Products";
import Transactions from "@/pages/Transactions";
import NotFound from "@/pages/not-found";

function MainContent() {
  const [location] = useLocation();

  return (
    <main className="flex-1 ml-60 overflow-auto">
      {location === "/" && <Dashboard />}
      {location === "/products" && <Products />}
      {location === "/transactions" && <Transactions />}
      {location !== "/" && location !== "/products" && location !== "/transactions" && <NotFound />}
    </main>
  );
}

function App() {
  const queryClient = React.useMemo(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 30_000,
            retry: (failureCount, error: any) => {
              if (error?.status >= 400 && error?.status < 500) return false;
              return failureCount < 2;
            },
            retryDelay: (attempt) =>
              Math.min(1000 * 2 ** attempt, 30000),
            networkMode: "always",
          },
          mutations: { retry: 1 },
        },
      }),
    []
  );

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="flex h-screen bg-background">
          {/* Sidebar */}
          <Sidebar />

          {/* Main content */}
          <MainContent />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
