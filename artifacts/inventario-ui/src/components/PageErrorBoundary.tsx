import { ReactNode, useEffect, useState } from "react";
import { AlertCircle } from "lucide-react";

interface PageErrorBoundaryProps {
  children: ReactNode;
  pageName?: string;
}

export function PageErrorBoundary({ children, pageName }: PageErrorBoundaryProps) {
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      console.error(`Error in ${pageName}:`, event.error);
      setError(event.error);
    };

    const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
      console.error(`Unhandled rejection in ${pageName}:`, event.reason);
      setError(new Error(String(event.reason)));
    };

    window.addEventListener("error", handleError);
    window.addEventListener("unhandledrejection", handleUnhandledRejection);

    return () => {
      window.removeEventListener("error", handleError);
      window.removeEventListener("unhandledrejection", handleUnhandledRejection);
    };
  }, [pageName]);

  if (error) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-background">
        <div className="w-full max-w-md mx-4 p-6 bg-card border border-border rounded-lg">
          <div className="flex items-start gap-3">
            <AlertCircle className="h-6 w-6 text-destructive flex-shrink-0 mt-0.5" />
            <div>
              <h1 className="text-lg font-semibold text-foreground">Error en {pageName || "la página"}</h1>
              <p className="mt-2 text-sm text-muted-foreground">
                {error?.message || "Algo salió mal."}
              </p>
              <button
                onClick={() => window.location.reload()}
                className="mt-4 px-4 py-2 bg-primary text-white rounded-md text-sm font-medium hover:bg-primary/90"
              >
                Recargar página
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
